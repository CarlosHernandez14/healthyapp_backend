from rest_framework import serializers
from .models import RegistroDiario

class RegistroDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDiario
        fields = '__all__'