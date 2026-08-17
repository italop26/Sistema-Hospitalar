from django.db import models
from pacientes.models import Paciente
from django.contrib.auth.models import User
from gestao_clinica.choices import Status
from gestao_clinica.especialidades import Especialidade
from gestao_clinica.turnos import Turno

from django.db import models



class Gestor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="gestor"
    )
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    is_gestor = models.BooleanField(default=True)
    is_chefe = models.BooleanField(default=False)

    def __str__(self):
        return self.nome



class ConfiguracaoVagas(models.Model):
    medico = models.ForeignKey('gestao_clinica.Medico', on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=20, choices=Especialidade.choices)
    turno = models.CharField(max_length=20, choices=Turno.choices)
    quantidade_vagas = models.PositiveIntegerField()# Mexe aqui ainda 

    class Meta:
        unique_together = ("especialidade", "turno")

    def __str__(self):
        return f"{self.get_especialidade_display()} - ({self.quantidade_vagas} vagas)"
        
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField()
    crm = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    especialidade = models.CharField(max_length=30, choices=Especialidade.choices)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_especialidade()}"


class GestaoDeAtendimento(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="atendimentos"
    )

    medico = models.ForeignKey('gestao_clinica.Medico',
        on_delete=models.CASCADE,
        related_name="atendimentos"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )

    data = models.DateTimeField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente} - {self.medico}"