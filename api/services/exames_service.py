from django.db import transaction
from core.models_exames import Exame
from medico.models import Medico
import random

class ExameService:

    @staticmethod
    @transaction.atomic
    def criar_exame(*, paciente, tipo_exame, data_exame):

        medico = ExameService.selecionar_medico(
            tipo_exame=tipo_exame,
            data_exame=data_exame
        )

        if medico is None:
            raise ValueError(
                "Não existe médico disponível para esse exame."
            )

        exame = Exame.objects.create(
            paciente=paciente,
            tipo_exame=tipo_exame,
            data_exame=data_exame,
            medico=medico.nome,
        )

        return exame

@staticmethod
def escolher_medico(*, tipo_exame, data):

        # 1. Busca os médicos que podem realizar o exame.
        medicos = Medico.objects.filter(
            # regra que relaciona médico ao tipo de exame
        )

        if not medicos.exists():
            return None

        # 2. Conta quantos exames cada médico possui.
        candidatos = []

        for medico in medicos:
            ocupado = Exame.objects.filter(
                    medico=medico.nome,
                    data=data
                ).exists()
            
            if ocupado:
                continue 
            
        quantidade_exames = Exame.objects.filter(
                    medico=medico.nome
                    ).count()

        quantidade_exames = Exame.objects.filter(
                medico=medico.nome
            ).count()

        candidatos.append({
                "medico": medico,
                "exames": quantidade_exames,
            })

        # 3. Prioriza quem possui menos exames.
        menor_quantidade = min(
            candidato["exames"]
            for candidato in candidatos
        )

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato["exames"] == menor_quantidade
        ]

        # 4. Se empatar, prioriza mais disponibilidades.
        maior_disponibilidade = max(
            candidato["medico"].quantidade_vagas
            for candidato in candidatos
        )

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato["medico"].vagas
            == maior_disponibilidade
        ]

        # 5. Se ainda empatar, escolha aleatória.
        escolhido = random.choice(candidatos)

        return escolhido["medico"]