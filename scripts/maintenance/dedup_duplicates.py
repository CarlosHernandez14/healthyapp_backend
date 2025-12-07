from django.db.models import Count
from citas.models import Cita
from registros.models import RegistroDiario

def dedup_citas():
    removed = 0
    duplicates = (
        Cita.objects.values('paciente_id', 'fecha', 'hora')
        .annotate(c=Count('id'))
        .filter(c__gt=1)
    )
    for g in duplicates:
        ids = list(
            Cita.objects.filter(
                paciente_id=g['paciente_id'],
                fecha=g['fecha'],
                hora=g['hora']
            )
            .order_by('id')
            .values_list('id', flat=True)
        )
        to_delete = ids[1:]  # keep the oldest by id, remove the rest
        if to_delete:
            Cita.objects.filter(id__in=to_delete).delete()
            removed += len(to_delete)
    return removed

def dedup_registros():
    removed = 0
    duplicates = (
        RegistroDiario.objects.values('cita_id', 'fecha')
        .annotate(c=Count('id'))
        .filter(c__gt=1)
    )
    for g in duplicates:
        ids = list(
            RegistroDiario.objects.filter(
                cita_id=g['cita_id'],
                fecha=g['fecha']
            )
            .order_by('id')
            .values_list('id', flat=True)
        )
        to_delete = ids[1:]  # keep the oldest by id, remove the rest
        if to_delete:
            RegistroDiario.objects.filter(id__in=to_delete).delete()
            removed += len(to_delete)
    return removed

# Execute immediately when run via `manage.py shell`
c_removed = dedup_citas()
r_removed = dedup_registros()
print(f"Removed {c_removed} duplicate Cita(s) and {r_removed} duplicate RegistroDiario(s)")
