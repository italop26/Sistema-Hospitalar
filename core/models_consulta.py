from django.db import models
from gestao_clinica.choices import Status
from pacientes.models import Paciente

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=200)
    medico = models.CharField(max_length=200)
    data = models.DateTimeField()
    status = models.CharField(max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )
    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_consulta}"



