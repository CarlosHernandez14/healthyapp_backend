from rest_framework import serializers
from .models import Cita

class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    paciente_apellido = serializers.CharField(source='paciente.apellido', read_only=True)
    # Override to bypass DRF's ChoiceField validation and let our normalization run first
    tipo = serializers.CharField()
    estado = serializers.CharField(required=False)
    # Accept UI alias 'notas' as a write-only field; will be mapped to tareas_iniciales on create/update
    notas = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Cita
        fields = [
            'id',
            'paciente',
            'paciente_nombre',
            'paciente_apellido',
            'fecha',
            'hora',
            'motivo',
            'notas',  # write-only alias -> mapped to tareas_iniciales
            'tipo',
            'estado',
            'objetivo_terapeutico',
            'enfoque_terapeutico',
            'plan_intervencion',
            'tareas_iniciales',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def to_internal_value(self, data):
        # Normalize incoming values BEFORE ChoiceField validation runs
        data = data.copy()

        # tipo: accept human labels/aliases and map to internal choices
        tipo_in = data.get('tipo')
        if isinstance(tipo_in, str):
            t = (tipo_in or '').strip().casefold()
            tipo_map = {
                'primera': 'primera',
                'primera vez': 'primera',
                'first': 'primera',
                'first time': 'primera',
                'seguimiento': 'seguimiento',
                'followup': 'seguimiento',
                'follow-up': 'seguimiento',
                'follow up': 'seguimiento',
            }
            if t in tipo_map:
                data['tipo'] = tipo_map[t]

        # estado: accept variants and map to internal choices
        estado_in = data.get('estado')
        if isinstance(estado_in, str):
            e = (estado_in or '').strip().casefold()
            estado_map = {
                'pendiente': 'pendiente',
                'asistida': 'asistida',
                'asistido': 'asistida',
                'cancelada': 'cancelada',
                'cancelado': 'cancelada',
            }
            if e in estado_map:
                data['estado'] = estado_map[e]

        return super().to_internal_value(data)

    def validate(self, attrs):
        paciente = attrs.get('paciente', getattr(self.instance, 'paciente', None))
        fecha = attrs.get('fecha', getattr(self.instance, 'fecha', None))
        hora = attrs.get('hora', getattr(self.instance, 'hora', None))

        if paciente and fecha and hora:
            # Validate uniqueness at the serializer level to produce a clean error
            from .models import Cita as CitaModel
            qs = CitaModel.objects.filter(paciente=paciente, fecha=fecha, hora=hora)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("El paciente ya tiene una cita en esa fecha y hora.")

        return attrs

    def create(self, validated_data):
        # Map 'notas' alias to tareas_iniciales on write
        notas = validated_data.pop('notas', None)
        instance = super().create(validated_data)
        if notas is not None:
            instance.tareas_iniciales = notas
            instance.save(update_fields=['tareas_iniciales'])
        return instance

    def update(self, instance, validated_data):
        # Map 'notas' alias to tareas_iniciales on write
        notas = validated_data.pop('notas', None)
        instance = super().update(instance, validated_data)
        if notas is not None:
            instance.tareas_iniciales = notas
            instance.save(update_fields=['tareas_iniciales'])
        return instance
