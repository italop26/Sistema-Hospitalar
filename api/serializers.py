from rest_framework import serializers
from core.models_consulta import Consulta
from core.models_exames import Exame

class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta

        fields = [
            "id",
            "paciente",
            "especialidade",
            "medico",
            "data_consulta",
            "status",
        ]

        read_only_fields = [
            "id",
            "paciente",
            "medico",
            "status",
        ]


class ExameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exame

        fields = [
            "id",
            "paciente",
            "data_exame",
            "tipo_exame",
            "medico",
            "status",
        ]

        read_only_fields = [
            "id",
            "paciente",
            "medico",
            "status",
        ]