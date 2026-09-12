from django.db import models

class Turno(models.TextChoices):
    MANHA = "MANHA", "Manhã"
    TARDE = "TARDE", "Tarde"
    NOITE = "NOITE", "Noite"


class DiaSemana(models.TextChoices):

    SEGUNDA = "SEG", "Segunda-feira"
    TERCA = "TER", "Terça-feira"
    QUARTA = "QUA", "Quarta-feira"
    QUINTA = "QUI", "Quinta-feira"
    SEXTA = "SEX", "Sexta-feira"
    SABADO = "SAB", "Sábado"
    DOMINGO = "DOM", "Domingo"