from rest_framework import serializers
from .models import Paciente, Consulta, Exame, StatusExame

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = '__all__'

class StatusExameSerializer(serializers.Serializer):
    class Meta:
        model = StatusExame
        fields = '__all__'