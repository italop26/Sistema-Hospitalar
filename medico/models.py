from django.db import models
from gestao_clinica.models import Medico
from pacientes.models import Paciente
from gestao_clinica.choices import Status

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="consultas")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADO)
    data = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta - {self.paciente} com {self.medico}"


class Exames(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="exames")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="exames")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADO)
    data = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exame - {self.paciente} com {self.medico}"


class Receitas(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="receitas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="receitas")
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receita - {self.paciente} de {self.medico}"
