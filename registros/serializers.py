from rest_framework import serializers
from .models import RegistroDiario, PlanAlimenticio

class RegistroDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDiario
        fields = '__all__'

class PlanAlimenticioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAlimenticio
        fields = '__all__'
