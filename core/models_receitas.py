from django.db import models
from .models_consulta import AtendimentoConsulta


class Receita(models.Model):
    atendimento = models.ForeignKey(
        AtendimentoConsulta,
        on_delete=models.CASCADE,
        related_name="receitas"
    )

    medicamento = models.CharField(max_length=200)
    dosagem = models.CharField(max_length=200)
    frequencia = models.CharField(max_length=200)
    duracao = models.CharField(max_length=200)
    observacoes = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"Receita do {self.atendimento}"