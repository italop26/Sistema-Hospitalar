from django.db import models

class Turno(models.TextChoices):
    MANHA = "MANHA", "Manhã"
    TARDE = "TARDE", "Tarde"
    NOITE = "NOITE", "Noite"
