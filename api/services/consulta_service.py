from django.db import transaction
import random

from core.models_consulta import Consulta
from medico.models import Medico
from gestao_clinica.models import HorarioMedico


class ConsultaService:

    @staticmethod
    @transaction.atomic
    def criar_consulta(
        *,
        paciente,
        tipo_consulta,
        especialidade,
        data,
        turno
    ):

        medico = ConsultaService.escolher_medico(
            tipo_consulta=tipo_consulta,
            especialidade=especialidade,
            data=data,
            turno=turno
        )

        if medico is None:
            raise ValueError(
                "Não existe médico disponível para essa consulta."
            )

        consulta = Consulta.objects.create(
            paciente=paciente,
            tipo_consulta=tipo_consulta,
            especialidade=especialidade,
            medico=medico,
            data=data,
            turno=turno
        )

        return consulta

    @staticmethod
    def escolher_medico(
        *,
        tipo_consulta,
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
            tipo_consulta=tipo_consulta,
            especialidade=especialidade,
            dia=dia,
            turno=turno,
            quantidade_vagas__gt=0,
            medico__ativo=True
        ).select_related("medico")

        # Não existe vaga configurada
        if not configuracoes.exists():
            return None

        candidatos = []

        # ==========================================
        # ANALISA CADA MÉDICO
        # ==========================================

        for configuracao in configuracoes:

            medico = configuracao.medico

            # Quantidade de consultas desse médico
            # nesse dia e nesse turno
            quantidade_consultas = Consulta.objects.filter(
                medico=medico,
                data__date=data,
                tipo_consulta=tipo_consulta,
                turno=turno
            ).count()

            # ======================================
            # VERIFICA LIMITE DE VAGAS
            # ======================================

            if quantidade_consultas >= configuracao.quantidade_vagas:
                continue

            candidatos.append({
                "medico": medico,
                "consultas": quantidade_consultas,
                "vagas": configuracao.quantidade_vagas
            })

        # ==========================================
        # NENHUM MÉDICO DISPONÍVEL
        # ==========================================

        if not candidatos:
            return None

        # ==========================================
        # 1º CRITÉRIO
        # MÉDICO COM MENOS CONSULTAS
        # ==========================================

        menor_quantidade = min(
            candidato["consultas"]
            for candidato in candidatos
        )

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato["consultas"] == menor_quantidade
        ]

        # ==========================================
        # 2º CRITÉRIO
        # MÉDICO COM MAIS VAGAS CONFIGURADAS
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