from django.db import models


class Especialidade(models.TextChoices):
    CLINICO = "CLINICO", "Clínico Geral"
    CARDIOLOGISTA = "CARDIO", "Cardiologista"
    DERMATOLOGISTA = "DERMA", "Dermatologista"
    PEDIATRA = "PED", "Pediatra"
    ORTOPEDISTA = "ORTO", "Ortopedista"
    GINECOLOGISTA = "GINE", "Ginecologista"
    PSIQUIATRA = "PSIQ", "Psiquiatra"


class TipoExame(models.TextChoices):
    HEMOGRAMA = "HEMOGRAMA", "Hemograma"
    RAIO_X = "RAIO_X", "Raio-X"
    TOMOGRAFIA = "TOMOGRAFIA", "Tomografia"
    ULTRASSOM = "ULTRASSOM", "Ultrassom"
    ELETROCARDIOGRAMA = "ELETROCARDIOGRAMA", "Eletrocardiograma"


class TipoConsulta(models.TextChoices):
    CLINICO = "CLINICO", "Clínico Geral"
    CARDIO = "CARDIO", "Cardiologista"
    DERMA = "DERMA", "Dermatologista"
    PED = "PED", "Pediatra"
    ORTO = "ORTO", "Ortopedista"
    GINE = "GINE", "Ginecologista"
    PSIQ = "PSIQ", "Psiquiatra"


TIPO_EXAME_ESPECIALIDADE = {
    TipoExame.HEMOGRAMA: Especialidade.CLINICO,
    TipoExame.RAIO_X: Especialidade.ORTOPEDISTA,
    TipoExame.TOMOGRAFIA: Especialidade.ORTOPEDISTA,
    TipoExame.ULTRASSOM: Especialidade.CLINICO,
    TipoExame.ELETROCARDIOGRAMA: Especialidade.CARDIOLOGISTA,
}