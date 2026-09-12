from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from gestao_clinica.models import Medico
from core.models_consulta import Consulta, AtendimentoConsulta
from core.models_exames import Exame, AtendimentoExame

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_medico(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "medico"):
            return redirect("medico:painel")

    if request.method == "POST":
        crm = request.POST.get("crm")
        senha = request.POST.get("senha")

        user = authenticate(
            request,
            username=crm,
            password=senha
        )

        if user is not None and hasattr(user, "medico"):
            login(request, user)

            return redirect("medico:painel")

        return render(
            request,
            "medico/login.html",
            {
                "erro": "CRM ou senha incorretos."
            }
        )

    return render(
        request,
        "medico/login.html"
    )

@login_required
def perfil_medico(request):
    medico = getattr(request.user, "medico", None)

    return render(
        request,
        'medico/perfil.html',
        {
            'medico': medico
        }
    )

    

@login_required
def painel_medico(request):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    agora = timezone.localtime()

    inicio_dia = agora.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    fim_dia = inicio_dia + timedelta(days=1)
    # Erro 
    consultas = Consulta.objects.filter(
        medico=medico,
        data__gte=inicio_dia,
        data__lt=fim_dia
    ).select_related("paciente")

    exames = Exame.objects.filter(
        medico=medico,
        data__gte=inicio_dia,
        data__lt=fim_dia
    ).select_related("paciente")

    atendimentos = []

    for consulta in consultas:

        if consulta.especialidade != medico.especialidade:
            continue

        atendimentos.append({
            "tipo": "consulta",
            "id": consulta.id,
            "paciente": consulta.paciente,
            "especialidade": consulta.especialidade,
            "data": consulta.data,
            "status": consulta.status,
        })

    for exame in exames:

        if exame.especialidade != medico.especialidade:
            continue

        atendimentos.append({
            "tipo": "exame",
            "id": exame.id,
            "paciente": exame.paciente,
            "especialidade": exame.especialidade,
            "data": exame.data,
            "status": exame.status,
        })

    atendimentos.sort(key=lambda item: item["data"])

    return render(
        request,
        "medico/painel.html",
        {
            "atendimentos": atendimentos,
        }
    )

@login_required
def iniciar_consulta(request, consulta_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    consulta = get_object_or_404(
        Consulta,
        id=consulta_id,
        medico=medico,
        especialidade=medico.especialidade
    )

    atendimento, criado = AtendimentoConsulta.objects.get_or_create(
        consulta=consulta,
        defaults={
            "paciente": consulta.paciente
        }
    )

    return render(
        request,
        "medico/atendimento_consulta.html",
        {
            "consulta": consulta,
            "atendimento": atendimento,
            "paciente": consulta.paciente,
            "especialidade": consulta.especialidade,
        }
    )

@login_required
def iniciar_exame(request, exame_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    exame = get_object_or_404(
        Exame,
        id=exame_id,
        medico=medico.nome,
        especialidade=medico.especialidade
    )

    atendimento, criado = AtendimentoExame.objects.get_or_create(
        exame=exame,
        defaults={
            "paciente": exame.paciente
        }
    )

    return render(
        request,
        "medico/atendimento_exame.html",
        {
            "exame": exame,
            "atendimento": atendimento,
            "paciente": exame.paciente,
            "especialidade": exame.especialidade,
        }
    )

@login_required
def salvar_atendimento_exame(request, exame_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    exame = get_object_or_404(
        Exame,
        id=exame_id,
        medico=medico.nome,
        especialidade=medico.especialidade
    )

    atendimento = get_object_or_404(
        AtendimentoExame,
        exame=exame
    )

    if request.method == "POST":

        atendimento.observacoes = request.POST.get(
            "observacoes",
            ""
        )

        atendimento.encaminhamento = request.POST.get(
            "encaminhamento",
            ""
        )

        atendimento.save()

        return redirect(
            "medico:confirmar_exame",
            exame_id=exame.id
        )

    return render(
        request,
        "medico/atendimento_exame.html",
        {
            "exame": exame,
            "atendimento": atendimento,
            "paciente": exame.paciente,
            "especialidade": exame.especialidade,
        }
    )

@login_required
def salvar_atendimento_consulta(request, consulta_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    consulta = get_object_or_404(
        Consulta,
        id=consulta_id,
        medico=medico.nome,
        especialidade=medico.especialidade
    )

    atendimento = get_object_or_404(
        AtendimentoConsulta,
        consulta=consulta
    )

    if request.method == "POST":

        atendimento.observacoes = request.POST.get(
            "observacoes",
            ""
        )

        atendimento.encaminhamento = request.POST.get(
            "encaminhamento",
            ""
        )

        atendimento.save()

        return redirect(
            "medico:confirmar_exame",
            consulta_id=consulta.id
        )

    return render(
        request,
        "medico/atendimento_exame.html",
        {
            "consulta": consulta,
            "atendimento": atendimento,
            "paciente": consulta.paciente,
            "especialidade": consulta.especialidade,
        }
    )

@login_required
def confirmar_consulta(request, consulta_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    consulta = get_object_or_404(
        Consulta,
        id=consulta_id,
        medico=medico.nome,
        especialidade=medico.especialidade
    )

    atendimento = get_object_or_404(
        AtendimentoConsulta,
        consulta=consulta
    )

    if request.method == "POST":

        senha = request.POST.get("senha")

        usuario = authenticate(
            request,
            username=request.user.username,
            password=senha
        )

        if usuario is None:

            return render(
                request,
                "medico/confirmar_atendimento.html",
                {
                    "erro": "Senha incorreta.",
                    "tipo": "consulta",
                    "objeto": consulta,
                }
            )

        atendimento.concluido_em = timezone.now()
        atendimento.save()

        # Coloque aqui o valor correto do seu Status
        consulta.status = "CONCLUIDO"
        consulta.save(update_fields=["status"])

        logout(request)

        return redirect(
            "gestao_clinica:login_medico"
        )

    return render(
        request,
        "medico/confirmar_atendimento.html",
        {
            "tipo": "consulta",
            "objeto": consulta,
        }
    )

@login_required
def confirmar_exame(request, exame_id):

    medico = getattr(request.user, "medico", None)

    if medico is None:
        return HttpResponseForbidden(
            "Usuário não possui acesso de médico."
        )

    exame = get_object_or_404(
        Exame,
        id=exame_id,
        medico=medico.nome,
        especialidade=medico.especialidade
    )

    atendimento = get_object_or_404(
        AtendimentoExame,
        exame=exame
    )

    if request.method == "POST":

        senha = request.POST.get("senha")

        usuario = authenticate(
            request,
            username=request.user.username,
            password=senha
        )

        if usuario is None:

            return render(
                request,
                "medico/confirmar_atendimento.html",
                {
                    "erro": "Senha incorreta.",
                    "tipo": "exame",
                    "objeto": exame,
                }
            )

        atendimento.concluido_em = timezone.now()
        atendimento.save()

        # Coloque aqui o valor correto do seu Status
        exame.status = "ANALISE"
        exame.data_conclusao = timezone.now()

        exame.save(
            update_fields=[
                "status",
                "data_conclusao"
            ]
        )

        logout(request)

        return redirect(
            "gestao_clinica:login_medico"
        )

    return render(
        request,
        "medico/confirmar_atendimento.html",
        {
            "tipo": "exame",
            "objeto": exame,
        }
    )

