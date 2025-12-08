from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from django.utils import timezone
from datetime import date, time, timedelta
from decimal import Decimal
import random
import os

from pacientes.models import Paciente
from citas.models import Cita
from registros.models import RegistroDiario


class Command(BaseCommand):
    help = "TRUNCATE domain data and repopulate the DB with coherent fake demo data for Pacientes, Citas and Registros."

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Required flag to proceed. This will DELETE existing Pacientes, Citas and Registros.",
        )
        parser.add_argument(
            "--n-pacientes",
            type=int,
            default=30,
            help="Number of Paciente records to create (default: 30).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed for reproducibility (default: None).",
        )
        parser.add_argument(
            "--dump",
            type=str,
            default=None,
            help="Optional fixtures path to dump generated data, e.g. fixtures/demo_seed.json",
        )

    def handle(self, *args, **options):
        if not options["confirm"]:
            raise CommandError("Refusing to run without --confirm. This command DELETES domain data.")

        n_pacientes = options["n_pacientes"]
        seed = options["seed"]
        dump_path = options["dump"]

        if seed is not None:
            random.seed(seed)

        with transaction.atomic():
            self._truncate_domain()
            self.stdout.write(self.style.WARNING("Existing domain data removed."))

            pacientes = self._create_pacientes(n_pacientes)
            self.stdout.write(self.style.SUCCESS(f"Created {len(pacientes)} pacientes."))

            citas = self._create_citas(pacientes)
            self.stdout.write(self.style.SUCCESS(f"Created {len(citas)} citas."))

            registros = self._create_registros(citas)
            self.stdout.write(self.style.SUCCESS(f"Created {len(registros)} registros diarios."))

        if dump_path:
            # Ensure directory
            os.makedirs(os.path.dirname(dump_path) or ".", exist_ok=True)
            # Dump only domain apps
            call_command(
                "dumpdata",
                "pacientes",
                "citas",
                "registros",
                output=dump_path,
                indent=2,
            )
            self.stdout.write(self.style.SUCCESS(f"Dump written to: {dump_path}"))

        self.stdout.write(self.style.SUCCESS("Reset and seed completed OK."))

    def _truncate_domain(self):
        # Delete in FK-safe order
        RegistroDiario.objects.all().delete()
        Cita.objects.all().delete()
        Paciente.objects.all().delete()

    def _create_pacientes(self, n):
        first_names_f = [
            "Ana", "Lucia", "Mariana", "Paola", "Laura", "Andrea", "Camila", "Valeria", "Sofia", "Daniela",
        ]
        first_names_m = [
            "Juan", "Carlos", "Luis", "Miguel", "Jorge", "Pedro", "Diego", "Andres", "Mateo", "Fernando",
        ]
        last_names = [
            "Lopez", "Garcia", "Martinez", "Hernandez", "Gonzalez", "Perez", "Rodriguez", "Sanchez", "Ramirez", "Flores",
        ]
        generos = ["M", "F", "O"]

        pacientes = []
        for i in range(n):
            if random.random() < 0.5:
                nombre = random.choice(first_names_f)
                genero = "F"
            else:
                nombre = random.choice(first_names_m)
                genero = "M"
            apellido = random.choice(last_names)
            edad = random.randint(18, 75)
            if random.random() < 0.1:
                genero = "O"  # some 'other' entries

            p = Paciente.objects.create(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                genero=genero,
            )
            pacientes.append(p)
        return pacientes

    def _create_citas(self, pacientes):
        enfoques = [
            "Mediterránea", "Alta proteína", "Baja en carbohidratos", "Vegetariana", "Balanceada", "DASH",
        ]
        estados = ["pendiente", "asistida", "cancelada"]
        tipos = ["primera", "seguimiento"]

        citas = []
        today = date.today()

        for p in pacientes:
            # 1 to 3 citas per paciente
            k = random.randint(1, 3)
            # Spread around past/future dates
            for _ in range(k):
                delta_days = random.randint(-30, 30)
                cita_fecha = today + timedelta(days=delta_days)
                # hour between 8:00 and 17:30
                hour = random.randint(8, 17)
                minute = random.choice([0, 15, 30, 45])
                cita_hora = time(hour=hour, minute=minute)

                objetivo = self._pick_objetivo_nutricional()
                enfoque = random.choice(enfoques)
                plan = self._pick_plan_alimentacion()
                recomendaciones = self._pick_recomendaciones()

                c = Cita.objects.create(
                    paciente=p,
                    fecha=cita_fecha,
                    hora=cita_hora,
                    motivo=self._pick_motivo(),
                    tipo=random.choice(tipos),
                    estado=random.choice(estados),
                    objetivo_nutricional=objetivo,
                    enfoque_nutricional=enfoque,
                    plan_alimentacion=plan,
                    recomendaciones=recomendaciones,
                )
                citas.append(c)
        return citas

    def _create_registros(self, citas):
        registros = []
        for c in citas:
            # Generate between 5 and 12 daily logs around the cita date (only for dates near cita)
            n = random.randint(5, 12)
            # pick a plausible base weight for the patient for this period
            base_weight = Decimal(random.randint(55, 95)) + Decimal(random.randint(0, 90)) / Decimal(100)

            start = c.fecha - timedelta(days=random.randint(0, 3))
            for i in range(n):
                d = start + timedelta(days=i)
                # Keep registros near current date range
                if d > date.today() + timedelta(days=7):
                    break

                cumplio = random.random() < 0.75
                adherencia = random.randint(60, 100) if cumplio else random.randint(30, 75)

                # slight daily variation in weight (±0.3 kg)
                jitter = Decimal(random.randint(-30, 30)) / Decimal(100)
                peso_kg = base_weight + jitter

                r = RegistroDiario.objects.create(
                    cita=c,
                    fecha=d,
                    cumplio=cumplio,
                    observaciones=self._pick_observacion(cumplio),
                    calorias=random.randint(1500, 2600) if random.random() < 0.85 else None,
                    agua_ml=random.randint(1500, 3500) if random.random() < 0.9 else None,
                    actividad_min=random.randint(0, 60) if random.random() < 0.8 else None,
                    peso_kg=peso_kg if random.random() < 0.7 else None,
                    adherencia=adherencia if random.random() < 0.95 else None,
                )
                registros.append(r)
        return registros

    def _pick_motivo(self):
        motivos = [
            "Plan nutricional por meta de peso",
            "Mejorar composición corporal",
            "Control de glucosa",
            "Mejorar rendimiento deportivo",
            "Mejorar hábitos alimenticios",
        ]
        return random.choice(motivos)

    def _pick_objetivo_nutricional(self):
        objetivos = [
            "Reducir 3kg en 8 semanas con déficit controlado",
            "Mejorar % músculo y bajar % grasa",
            "Controlar apetito y mejorar saciedad",
            "Optimizar energía durante el día",
            "Reducir perímetro abdominal",
        ]
        return random.choice(objetivos)

    def _pick_plan_alimentacion(self):
        planes = [
            "Menú 3 comidas + 2 colaciones",
            "Menú semanal con colación alta en proteína",
            "Plan mediterráneo con déficit 15%",
            "Plan vegetariano con foco en proteína vegetal",
            "Plan balanceado con distribución 40/30/30",
        ]
        return random.choice(planes)

    def _pick_recomendaciones(self):
        recs = [
            "Beber 2L de agua/día; evitar azúcares añadidos",
            "7000 pasos/día; 2L agua/día",
            "Incluir verduras en 2/3 comidas del día",
            "Evitar bebidas azucaradas; preferir infusiones",
            "Cenar al menos 2 horas antes de dormir",
        ]
        return random.choice(recs)

    def _pick_observacion(self, cumplio: bool):
        if cumplio:
            obs = [
                "Buen apego al plan",
                "Sin hambre nocturna",
                "Energía estable durante el día",
                "Buen control de antojos",
            ]
        else:
            obs = [
                "Dificultad para cumplir colación",
                "Hambre nocturna",
                "Apetito alto por estrés",
                "Se omitió actividad física",
            ]
        return random.choice(obs)
