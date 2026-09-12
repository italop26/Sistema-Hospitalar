from django.db import transaction
import random

from core.models_exames import Exame
from medico.models import Medico
from gestao_clinica.models import HorarioMedico
from gestao_clinica.especialidades import TIPO_EXAME_ESPECIALIDADE


class ExameService:

    @staticmethod
    @transaction.atomic
    def criar_exame(
        *,
        paciente,
        tipo_exame,
        data,
        turno
    ):

        # ==========================================
        # DESCOBRE A ESPECIALIDADE PELO TIPO DO EXAME
        # ==========================================

        especialidade = TIPO_EXAME_ESPECIALIDADE.get(
            tipo_exame
        )

        if especialidade is None:
            raise ValueError(
                "Não existe especialidade configurada para esse exame."
            )

        # ==========================================
        # ESCOLHE O MÉDICO
        # ==========================================

        medico = ExameService.escolher_medico(
            tipo_exame=tipo_exame,
            especialidade=especialidade,
            data=data,
            turno=turno
        )

        if medico is None:
            raise ValueError(
                "Não existe médico disponível para esse exame."
            )

        # ==========================================
        # CRIA O EXAME
        # ==========================================

        exame = Exame.objects.create(
            paciente=paciente,
            tipo_exame=tipo_exame,
            especialidade=especialidade,
            medico=medico,
            data=data,
            turno=turno
        )

        return exame

    @staticmethod
    def escolher_medico(
        *,
        tipo_exame,
        especialidade,
        data,
        turno
    ):

        # ==========================================
        # CONVERTE DATA → DIA DA SEMANA
        # ==========================================

        dias = {
            0: "SEG",
            1: "TER",
            2: "QUA",
            3: "QUI",
            4: "SEX",
            5: "SAB",
            6: "DOM",
        }

        dia = dias[data.weekday()]

        # ==========================================
        # BUSCA AS VAGAS CRIADAS PELA GESTÃO
        # ==========================================

        configuracoes = HorarioMedico.objects.filter(
            tipo_exame=tipo_exame,
            especialidade=especialidade,
            dia=dia,
            turno=turno,
            quantidade_vagas__gt=0,
            medico__ativo=True
        ).select_related("medico")

        if not configuracoes.exists():
            return None

        candidatos = []

        # ==========================================
        # ANALISA CADA MÉDICO
        # ==========================================

        for configuracao in configuracoes:

            medico = configuracao.medico

            # Quantidade de exames desse médico
            # nesse dia e nesse turno
            quantidade_exames = Exame.objects.filter(
                medico=medico,
                data__date=data,
                turno=turno
            ).count()

            # ======================================
            # VERIFICA LIMITE DE VAGAS
            # ======================================

            if quantidade_exames >= configuracao.quantidade_vagas:
                continue

            candidatos.append({
                "medico": medico,
                "exames": quantidade_exames,
                "vagas": configuracao.quantidade_vagas
            })

        # ==========================================
        # NENHUM MÉDICO DISPONÍVEL
        # ==========================================

        if not candidatos:
            return None

        # ==========================================
        # 1º CRITÉRIO
        # MÉDICO COM MENOS EXAMES
        # ==========================================

        menor_quantidade = min(
            candidato["exames"]
            for candidato in candidatos
        )

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato["exames"] == menor_quantidade
        ]

        # ==========================================
        # 2º CRITÉRIO
        # MÉDICO COM MAIS VAGAS
        # ==========================================

        maior_quantidade_vagas = max(
            candidato["vagas"]
            for candidato in candidatos
        )

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato["vagas"] == maior_quantidade_vagas
        ]

        # ==========================================
        # 3º CRITÉRIO
        # EMPATE → ALEATÓRIO
        # ==========================================

        escolhido = random.choice(candidatos)

        return escolhido["medico"]