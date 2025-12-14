from rest_framework import serializers

from .models import Cita


class CitaSerializer(serializers.ModelSerializer):
    # Lectura: campos derivados para evitar lookups en UI
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    paciente_apellido = serializers.CharField(source='paciente.apellido', read_only=True)
    plan_resumen = serializers.SerializerMethodField(read_only=True)
    # Alias "notas" para mapear al campo recomendaciones (lectura/escritura)
    notas = serializers.CharField(source='recomendaciones', required=False, allow_null=True, allow_blank=True)
    # Alias de compatibilidad (solo escritura) para clientes antiguos (psicología)
    objetivo_terapeutico = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    enfoque_terapeutico = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    plan_intervencion = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    tareas_iniciales = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)

    class Meta:
        model = Cita
        fields = '__all__'

    def get_plan_resumen(self, obj):
        partes = []
        if getattr(obj, 'motivo', None):
            partes.append(f"Motivo: {obj.motivo}")
        if getattr(obj, 'objetivo_nutricional', None):
            partes.append(f"Objetivo nutricional: {obj.objetivo_nutricional}")
        if getattr(obj, 'enfoque_nutricional', None):
            partes.append(f"Enfoque nutricional: {obj.enfoque_nutricional}")
        if getattr(obj, 'plan_alimentacion', None):
            partes.append(f"Plan de alimentación: {obj.plan_alimentacion}")
        if getattr(obj, 'recomendaciones', None):
            partes.append(f"Recomendaciones: {obj.recomendaciones}")
        return " | ".join(partes) if partes else None

    def validate(self, attrs):
        # Aceptar valores legacy y aliasar campos
        # 1) Mapear claves antiguas a los campos nuevos nutricionales si no se enviaron explícitamente
        legacy_to_new = {
            'objetivo_terapeutico': 'objetivo_nutricional',
            'enfoque_terapeutico': 'enfoque_nutricional',
            'plan_intervencion': 'plan_alimentacion',
            'tareas_iniciales': 'recomendaciones',
        }
        for legacy, new in legacy_to_new.items():
            if legacy in attrs and (new not in attrs or attrs.get(new) in (None, '')):
                attrs[new] = attrs.get(legacy)

        # 2) Normalizar el tipo para aceptar etiquetas humanas desde el frontend
        tipo = attrs.get('tipo')
        if isinstance(tipo, str):
            val = tipo.strip().lower()
            label_to_value = {
                'primera vez': 'primera',
                'seguimiento': 'seguimiento',
            }
            # también aceptar directamente 'primera'/'seguimiento'
            if val in label_to_value:
                attrs['tipo'] = label_to_value[val]
            elif val in ('primera', 'seguimiento'):
                attrs['tipo'] = val

        return attrs
