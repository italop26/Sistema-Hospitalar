from django.db import models
from gestao_clinica.models import Medico
from pacientes.models import Paciente



class Receitas(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="receitas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="receitas")
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receita - {self.paciente} de {self.medico}"
