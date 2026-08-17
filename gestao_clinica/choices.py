from django.db import models

class Status(models.TextChoices):
    AGENDADO = "AGENDADO", "Agendado"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    FINALIZADO = "FINALIZADO", "Finalizado"
    CANCELADO = "CANCELADO", "Cancelado"
    ADIADO = 'ADIADO', 'adiado'
    EM_ANALISE = 'EM_ANALISE', 'em_analise'
