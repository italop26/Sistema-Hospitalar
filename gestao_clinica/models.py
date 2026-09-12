from django.db import models
from pacientes.models import Paciente
from django.contrib.auth.models import User
from gestao_clinica.choices import Status
from gestao_clinica.especialidades import Especialidade, TipoExame, TipoConsulta
from gestao_clinica.turnos import Turno, DiaSemana
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=254)
    idade = models.IntegerField()
    crm = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    especialidade = models.CharField(max_length=30, choices=Especialidade.choices)
    exames = models.JSONField(
    default=list,
    blank=True
)

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.especialidade}"

class HorarioMedico(models.Model):

    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="horarios"
    )
    especialidade = models.CharField(max_length=20, choices=Especialidade.choices, null=True,
        blank=True)

    tipo_consulta = models.CharField(
        max_length=30,
        choices=TipoConsulta.choices,
        null=True,
        blank=True
    )

    tipo_exame = models.CharField(
    max_length=30,
    choices=TipoExame.choices,
    null=True,
    blank=True
)

    dia = models.CharField(
        max_length=3,
        choices=DiaSemana.choices
    )

    turno = models.CharField(
        max_length=10,
        choices=Turno.choices
    )
    quantidade_vagas = models.PositiveIntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(50),
        ], default=0)

    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=[
                "medico",
                "dia",
                "turno",
                "especialidade",
                "tipo_consulta",
                "tipo_exame",
            ],
            name="unique_medico_dia_turno_tipo"
        )
    ]

    def __str__(self):

        if self.tipo_consulta:
            tipo = self.get_tipo_consulta_display()

        elif self.tipo_exame:
            tipo = self.get_tipo_exame_display()

        else:
            tipo = "Configuração sem tipo"

        return (
        f"{self.medico.nome} - "
        f"{tipo} - "
        f"{self.get_dia_display()} - "
        f"{self.get_turno_display()}"
    )


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