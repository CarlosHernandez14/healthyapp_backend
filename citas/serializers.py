from rest_framework import serializers
from .models import Cita

class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    paciente_apellido = serializers.CharField(source='paciente.apellido', read_only=True)

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
            'tipo',
            'estado',
            'objetivo_terapeutico',
            'enfoque_terapeutico',
            'plan_intervencion',
            'tareas_iniciales',
            'created_at',
        ]
        read_only_fields = ['created_at']

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
