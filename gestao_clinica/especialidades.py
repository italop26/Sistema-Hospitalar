from django.db import models

class Especialidade(models.TextChoices):
        CLINICO = "CLINICO", "Clínico Geral"
        CARDIOLOGISTA = "CARDIO", "Cardiologista"
        DERMATOLOGISTA = "DERMA", "Dermatologista"
        PEDIATRA = "PED", "Pediatra"
        ORTOPEDISTA = "ORTO", "Ortopedista"
        GINECOLOGISTA = "GINE", "Ginecologista"
        PSIQUIATRA = "PSIQ", "Psiquiatra"
