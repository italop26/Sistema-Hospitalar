from django.db import models
from gestao_clinica.choices import Status
from pacientes.models import Paciente
from gestao_clinica.especialidades import TipoExame
from gestao_clinica.models import Medico
from gestao_clinica.turnos import Turno

class Exame(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )

    data = models.DateTimeField()

    tipo_exame = models.CharField(
        max_length=30,
        choices=TipoExame.choices
    )



    especialidade = models.CharField(
        max_length=30
    )

    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        related_name="exames_realizados"
    )

    turno = models.CharField(
        max_length=20,
        choices=Turno.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )

    data_conclusao = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Exame de {self.paciente.nome} em {self.data}"

class AtendimentoExame(models.Model):
    exame = models.OneToOneField(
        Exame,
        on_delete=models.CASCADE,
        related_name="atendimento"
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="atendimentos_exame"
    )

    observacoes = models.TextField(blank=True)
    encaminhamento = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    concluido_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Atendimento do exame - {self.exame.paciente.nome}"