from django.db import transaction
from core.models_consulta import Consulta
from medico.models import Medico
import random


class ConsultaService:

    @staticmethod
    @transaction.atomic
    def criar_consulta(*, paciente, especialidade, data):

        medico = ConsultaService.selecionar_medico(
            especialidade=especialidade,
            data_consulta=data
        )

        if medico is None:
            raise ValueError(
                "Não existe médico disponível para essa consulta."
            )

        consulta = Consulta.objects.create(
            paciente=paciente,
            especialidade=especialidade,
            medico=medico.nome,
            data_consulta=data,
        )

        return consulta

@staticmethod
def escolher_medico(*, especialidade, data):

    # 1. Busca todos os médicos da especialidade.
    medicos = Medico.objects.filter(
        especialidade=especialidade
    )

    if not medicos.exists():
        return None

        # 2. Verifica quantas consultas cada médico possui.
    candidatos = []

    for medico in medicos:
        ocupado = Consulta.objects.filter(
        medico=medico.nome,
        data=data
    ).exists()

        if ocupado:
            continue 

    quantidade_consultas = Consulta.objects.filter(
        medico=medico.nome
        ).count()

    candidatos.append({
    "medico": medico,
    "consultas": quantidade_consultas,
})

# 3. Descobre o menor número de consultas.
    menor_quantidade = min(
    candidato["consultas"]
    for candidato in candidatos
)

    candidatos = [
    candidato
    for candidato in candidatos
    if candidato["consultas"] == menor_quantidade
]

# 4. Se ainda houver empate,
# verifica quem possui mais vagas.
    maior_disponibilidade = max(
    candidato["medico"].quantidade_vagas
    for candidato in candidatos
)

    candidatos = [
    candidato
    for candidato in candidatos
    if candidato["medico"].quantidade_vagas == maior_disponibilidade
]

# 5. Se ainda houver empate,
# escolhe aleatoriamente.
    escolhido = random.choice(candidatos)
    return escolhido["medico"]