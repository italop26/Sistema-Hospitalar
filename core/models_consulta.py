from django.db import models
from gestao_clinica.choices import Status
from pacientes.models import Paciente
from gestao_clinica.especialidades import TipoConsulta, Especialidade
from gestao_clinica.turnos import Turno
from gestao_clinica.models import Medico


class Consulta(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )

    tipo_consulta = models.CharField(
        max_length=30,
        choices=TipoConsulta.choices
    )

    especialidade = models.CharField(
        max_length=30,
        choices=Especialidade.choices
    )

    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        related_name="consultas"
    )

    data = models.DateTimeField()

    turno = models.CharField(
        max_length=10,
        choices=Turno.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data}"

class AtendimentoConsulta(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name="atendimento"
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="atendimentos_consulta"
    )
    queixa_principal = models.CharField(max_length=500, blank=True)
    sintomas = models.CharField(max_length=1000, blank=True)
    diagnostico = models.CharField(max_length=1000, blank=True)
    conduta = models.CharField(max_length=1000, blank=True)
    prescricao = models.CharField(max_length=1000, blank=True)
    retorno = models.CharField(max_length=500, blank=True)
    observacoes = models.CharField(max_length=1000, blank=True)
    observacoes = models.TextField(blank=True)
    encaminhamento = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    concluido_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Atendimento da consulta - {self.consulta.paciente.nome}"



