from django.db import models
from django.contrib.auth.models import User
from gestao_clinica.choices import Status


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    data_nascimento = models.DateField()
    historico_medico = models.TextField()
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.nome
    
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=200)
    medico = models.CharField(max_length=200)
    data_consulta = models.DateTimeField()
    status = models.CharField(max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )
    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_consulta}"



class Exame(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_exame = models.DateTimeField()
    tipo_exame = models.CharField(max_length=100)
    medico = models.CharField(max_length=200)
    status = models.CharField(max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO
    )
    def __str__(self):
        return f"Exame de {self.paciente.nome} em {self.data_exame}"