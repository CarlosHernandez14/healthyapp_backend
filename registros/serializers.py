from rest_framework import serializers
from .models import RegistroDiario

class RegistroDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDiario
        fields = '__all__'

    def validate(self, attrs):
        cita = attrs.get('cita', getattr(self.instance, 'cita', None))
        fecha = attrs.get('fecha', getattr(self.instance, 'fecha', None))

        if cita and fecha:
            qs = RegistroDiario.objects.filter(cita=cita, fecha=fecha)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Registro diario para esta cita y fecha ya existe.")

        return attrs
