from django.db import models
from gestao_clinica.choices import Status
from pacientes.models import Paciente

class Exame(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField()    
    especialidade = models.CharField(max_length=100)
    medico = models.CharField(max_length=200)
    status = models.CharField(max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )
    data_conclusao = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Exame de {self.paciente.nome} em {self.data}"