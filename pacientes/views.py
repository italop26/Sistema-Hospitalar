from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Paciente
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from core.models_exames import Exame
from core.models_consulta import Consulta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from api.services.consulta_service import ConsultaService
from api.services.exames_service import ExameService
from datetime import datetime
from gestao_clinica.models import HorarioMedico
from gestao_clinica.especialidades import TIPO_EXAME_ESPECIALIDADE
from core.models_receitas import Receita
from core.models_consulta import AtendimentoConsulta
from core.models_exames import AtendimentoExame


def login_view(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        user = authenticate(
            request,
            username=cpf,
            password=senha
        )
        
        if user:
            login(request, user)
            
            return redirect('principal')
        
        return HttpResponse("CPF ou senha inválidos")
    return render(request, 'paciente/login.html')
        

def criar_conta(request):
    if request.method == 'POST':

        user = User.objects.create_user(
            username = request.POST.get('cpf'),
            password = request.POST.get('senha')
        )

        paciente = Paciente.objects.create(
        user=user,
        nome = request.POST.get('nome'),
        idade = request.POST.get('idade'),
        email = request.POST.get('email'),
        telefone = request.POST.get('telefone'),
        data_nascimento = request.POST.get('data_nascimento'),
        cpf= request.POST.get('cpf')
        )
        if paciente:
            return redirect('login')
        return HttpResponse('Erro ao criar conta')
    return render(request, 'paciente/criar_conta.html')

def principal(request):

    if request.user.is_authenticated:
        paciente = request.user.paciente

        consultas = Consulta.objects.filter(paciente=paciente)
        exames = Exame.objects.filter(paciente=paciente)

    return render(
        request,
        'paciente/principal.html',
        {
            'paciente': paciente,
            'consultas': consultas,
            'exames': exames,
        }
    )
    
@login_required
def marcacao(request):

    paciente = request.user.paciente

    tipo = request.GET.get("tipo", "consulta")

    # =====================================================
    # POST — AGENDAMENTO
    # =====================================================

    if request.method == "POST":

        tipo = request.POST.get("tipo")

        # =================================================
        # CONSULTA
        # =================================================

        if tipo == "consulta":

            tipo_consulta = request.POST.get("tipo_consulta")
            data = request.POST.get("data")
            turno = request.POST.get("turno")

            try:

                data = datetime.strptime(
                    data,
                    "%Y-%m-%d"
                ).date()

                # TipoConsulta e Especialidade possuem
                # os mesmos valores.
                especialidade = tipo_consulta

                medico = ConsultaService.escolher_medico(
                    especialidade=especialidade,
                    data=data,
                    tipo_consulta=tipo_consulta,
                    turno=turno
                )

                if medico is None:

                    messages.error(
                        request,
                        "Não existe médico disponível para essa consulta."
                    )

                    return redirect(
                        f"{request.path}?tipo=consulta"
                    )

                Consulta.objects.create(
                    paciente=paciente,
                    tipo_consulta=tipo_consulta,
                    especialidade=especialidade,
                    data=data,
                    turno=turno,
                    medico=medico
                )

                messages.success(
                    request,
                    "Consulta agendada com sucesso."
                )

            except ValueError as erro:

                messages.error(
                    request,
                    str(erro)
                )

                return redirect(
                    f"{request.path}?tipo=consulta"
                )

        # =================================================
        # EXAME
        # =================================================

        elif tipo == "exame":

            tipo_exame = request.POST.get("tipo_exame")
            data = request.POST.get("data")
            turno = request.POST.get("turno")

            try:

                data = datetime.strptime(
                    data,
                    "%Y-%m-%d"
                ).date()

                # A especialidade NÃO é escolhida manualmente.
                # Ela é definida pelo tipo do exame.
                especialidade = TIPO_EXAME_ESPECIALIDADE.get(
                    tipo_exame
                )

                if not especialidade:

                    messages.error(
                        request,
                        "Não foi possível identificar a especialidade desse exame."
                    )

                    return redirect(
                        f"{request.path}?tipo=exame"
                    )

                medico = ExameService.escolher_medico(
                    tipo_exame=tipo_exame,
                    especialidade=especialidade,
                    data=data,
                    turno=turno
                )

                if medico is None:

                    messages.error(
                        request,
                        "Não existe médico disponível para esse exame."
                    )

                    return redirect(
                        f"{request.path}?tipo=exame"
                    )

                Exame.objects.create(
                    paciente=paciente,
                    tipo_exame=tipo_exame,
                    especialidade=especialidade,
                    data=data,
                    turno=turno,
                    medico=medico
                )

                messages.success(
                    request,
                    "Exame agendado com sucesso."
                )

            except ValueError as erro:

                messages.error(
                    request,
                    str(erro)
                )

                return redirect(
                    f"{request.path}?tipo=exame"
                )

        return redirect("principal")

    # =====================================================
    # GET — VAGAS CRIADAS PELA GESTÃO
    # =====================================================

    data_selecionada = request.GET.get("data")

    consultas_disponiveis = []
    exames_disponiveis = []

    if data_selecionada:

        try:

            data = datetime.strptime(
                data_selecionada,
                "%Y-%m-%d"
            ).date()

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

            horarios = HorarioMedico.objects.filter(
                dia=dia,
                quantidade_vagas__gt=0
            )

            # ---------------------------------------------
            # CONSULTAS
            # ---------------------------------------------

            consultas_disponiveis = horarios.filter(
                tipo_consulta__isnull=False
            ).exclude(
                tipo_consulta=""
            ).values(
                "tipo_consulta",
                "turno"
            ).distinct()

            # ---------------------------------------------
            # EXAMES
            # ---------------------------------------------

            exames_disponiveis = horarios.filter(
                tipo_exame__isnull=False
            ).exclude(
                tipo_exame=""
            ).values(
                "tipo_exame",
                "turno"
            ).distinct()

        except ValueError:
            pass

    context = {
        "tipo": tipo,

        "data_selecionada": data_selecionada or "",

        "consultas_disponiveis":
            consultas_disponiveis,

        "exames_disponiveis":
            exames_disponiveis,
    }

    return render(
        request,
        "paciente/marcacao.html",
        context
    )
            
        

def perfil(request):
    if request.user.is_authenticated:

        paciente = request.user.paciente
        return render(request, 'paciente/perfil.html', {'paciente': paciente})
        
           
    else:
        return HttpResponse('Erro')

def ver_exames(request):
    paciente = request.user.paciente
    exames = Exame.objects.filter(paciente=paciente)
    paginator = Paginator(exames, 10)
    page = request.GET.get("page")

    exames = paginator.get_page(page)
    return render(request, 'paciente/ver_exames.html', {'exames': exames})

def ver_consultas(request):
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente)
    paginator = Paginator(consultas, 10)
    page = request.GET.get("page")

    consultas = paginator.get_page(page)
    return render(request, 'paciente/ver_consultas.html', {'consultas': consultas})

def sair(request):
    logout(request)
    return redirect('login')

@login_required
def receitas(request):
    paciente = get_object_or_404(
        Paciente,
        user=request.user
    )

    receitas = Receita.objects.filter(
        atendimento__paciente=paciente
    ).select_related(
        "atendimento"
    )

    return render(
        request,
        "paciente/receitas.html",
        {"receitas": receitas,
         'paciente': paciente}
    )
    
@login_required
def meus_atendimentos(request):
    
    paciente = get_object_or_404(
        Paciente,
        user=request.user
    )

    consultas = AtendimentoConsulta.objects.filter(
        paciente=paciente
    )

    exames = AtendimentoExame.objects.filter(
        paciente=paciente
    )

    return render(
        request,
        "paciente/atendimentos.html",
        {
            "consultas": consultas,
            "exames": exames,
            'paciente': paciente
        }
    )

@login_required
def ver_atendimento_consulta(request, consulta_id):
    paciente = get_object_or_404(
        Paciente,
        user=request.user
    )

    consulta = get_object_or_404(
        AtendimentoConsulta,
        id=consulta_id,
        paciente=paciente
    )


    return render(
        request,
        "paciente/atendimento_consulta.html",
        {
            "consulta": consulta,
            'paciente': paciente
        }
    )

@login_required
def ver_resultado_exame(request, exame_id):

    paciente = get_object_or_404(
        Paciente,
        user=request.user
    )

    exame = get_object_or_404(
        AtendimentoExame,
        id=exame_id,
        paciente=paciente
    )

    if exame.status != "concluido":
        return render(
            request,
            "paciente/resultado_exame.html",
            {
                "exame": exame,
                "disponivel": False,
                "paciente": paciente
            }
        )

    return render(
        request,
        "paciente/ver_resultado_exame.html",
        {
            "exame": exame,
            "disponivel": True,
            "paciente": paciente
        }
    )
    
