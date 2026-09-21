from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from gestao_clinica.choices import Status 
from gestao_clinica.especialidades import Especialidade, TipoConsulta, TipoExame
from .models import Gestor, TipoExame, HorarioMedico
from gestao_clinica.turnos import Turno, DiaSemana
from django.contrib.auth.models import User
from medico.models import Medico
from .models import Especialidade
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from datetime import timedelta, date
from django.utils import timezone
from pacientes.models import Paciente
from core.models_consulta import Consulta
from core.models_exames import Exame
from api.autenticaçao.jwt import gerar_token

#Login do adm 



def login_gestor(request):

     if request.method == "POST":
         username = request.POST.get("username")
         senha = request.POST.get("senha")

         user = authenticate(
         request,
         username=username,
         password=senha)

         if user is not None:

            token = gerar_token(user)

            login(request, user)

            response = redirect("gestao_clinica:dashbord")

            response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=False,  # True quando estiver usando HTTPS
            samesite="Lax"
    )

            return response

         if not username or not senha:
             return render(request, "gestao/login.html", {
                             "erro": "preencha os campos correto ."
                         })
            

         if user is None:
             return render(request, "gestao/login.html", {
                 "erro": "Usuário ou senha inválidos."
             })

         if not hasattr(user, "gestor"):
                return render(request, "gestao/login.html", {
                "erro": "Este usuário não possui acesso à gestão."
             })
    
     return render(request, "gestao/login.html")


def logout_gestor(request):
     logout(request)
     return redirect("gestao_clinica:login_gestor")

@login_required
def criar_gestor(request):
    if not request.user.gestor.is_chefe:
        return HttpResponseForbidden("Acesso negado")

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        username = request.POST.get("username", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")
        is_chefe = request.POST.get('Gestor_adm') == 'on'

        if not all([nome, username, senha, confirmar_senha, is_chefe]):
            return render(request, "gestao_clinica/cadastrar_gestor.html", {
                "erro": "Preencha todos os campos."
            })

        if senha != confirmar_senha:
            return render(request, "gestao_clinica/cadastrar_gestor.html", {
                "erro": "As senhas não coincidem."
            })

        if len(senha) < 8:
            return render(request, "gestao_clinica/cadastrar_gestor.html", {
                "erro": "A senha deve ter pelo menos 8 caracteres."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "gestao_clinica/cadastrar_gestor.html", {
                "erro": "Esse nome de usuário já está em uso."
            })

        try:
            user = User.objects.create_user(
                username=username,
                password=senha
            )

            Gestor.objects.create(
                user=user,
                nome=nome,
                is_chefe=is_chefe
            )

        except IntegrityError:
            return render(request, "gestao_clinica/criar_gestor.html", {
                "erro": "Não foi possível cadastrar o gestor."
            })

        return redirect("gestao_clinica:dashbord")

    return render(request, "gestao/criar_gestor.html")

def excluir_gestor(request, gestor_id):
    if not request.user.is_authenticated:
        return redirect("gestao_clinica:login_gestor")

    if not request.user.gestor.is_chefe:
        return HttpResponseForbidden("Acesso negado.")

    gestor = get_object_or_404(Gestor, id=gestor_id)

    if request.method == "POST":
        user = gestor.user
        gestor.delete()
        user.delete()

        return redirect("gestao_clinica:dashbord")

    return render(request,"gestao/excluir_gestor.html")


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):

    agora = timezone.localtime()
    hoje = agora.date()

    # =====================================================
    # PERÍODO DO DASHBOARD
    # =====================================================

    data_inicial = hoje - timedelta(days=5)
    data_final = hoje + timedelta(days=4)

    consultas = (
        Consulta.objects
        .filter(data__date__range=(data_inicial, data_final))
        .select_related("paciente")
        .order_by("data")
    )

    exames = (
        Exame.objects
        .filter(data__date__range=(data_inicial, data_final))
        .select_related("paciente")
        .order_by("data")
    )

    # =====================================================
    # QUANTIDADES
    # =====================================================

    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.count()
    total_gestores = Gestor.objects.count()

    consultas_de_hoje = Consulta.objects.filter(
        data__date=hoje
    ).count()

    exames_de_hoje = Exame.objects.filter(
        data__date=hoje
    ).count()

    # =====================================================
    # DIAS DO DASHBOARD
    # =====================================================

    dias = []

    data_atual = data_inicial

    while data_atual <= data_final:

        consultas_do_dia = [
            consulta
            for consulta in consultas
            if timezone.localtime(consulta.data).date() == data_atual
        ]

        exames_do_dia = [
            exame
            for exame in exames
            if timezone.localtime(exame.data).date() == data_atual
        ]

        dias.append({
            "data": data_atual,
            "hoje": data_atual == hoje,

            "consultas": consultas_do_dia,
            "exames": exames_do_dia,

            "total_consultas": len(consultas_do_dia),
            "total_exames": len(exames_do_dia),

            "total": (
                len(consultas_do_dia)
                + len(exames_do_dia)
            ),
        })

        data_atual += timedelta(days=1)

    # =====================================================
    # CONTEXTO
    # =====================================================

    context = {
        "dias": dias,

        "data_inicial": data_inicial,
        "data_final": data_final,
        "hoje": hoje,

        "pacientes": total_pacientes,
        "medicos": total_medicos,
        "gestores": total_gestores,

        "consultas_de_hoje": consultas_de_hoje,
        "exames_de_hoje": exames_de_hoje,
    }

    return render(
        request,
        "gestao/dashbord.html",
        context
    )
@login_required
def criar_medico(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        email = request.POST.get("email")
        idade = request.POST.get("idade")
        crm = request.POST.get("crm")
        cpf = request.POST.get("cpf")
        especialidade = request.POST.get("especialidade")

        exames = request.POST.getlist("exames")

        if not all([
            nome,
            idade,
            crm,
            cpf,
            especialidade,
            email
        ]):
            messages.error(
                request,
                "Preencha todos os campos obrigatórios."
            )
            return redirect(
                "gestao_clinica:criar_medico"
            )


        if Medico.objects.filter(crm=crm).exists():
            messages.error(
                request,
                "Já existe um médico com esse CRM."
            )
            return redirect(
                "gestao_clinica:criar_medico"
            )

        user = User.objects.create_user(
            username=crm,
            password=request.POST.get("senha"),
        )

        medico = Medico.objects.create(
            user=user,
            nome=nome,
            idade=idade,
            email=email,
            crm=crm,
            cpf=cpf,
            especialidade=especialidade,
            exames=exames
        )

        # Cria as combinações de dia + turno

        messages.success(
            request,
            f"Médico {nome} cadastrado com sucesso."
        )

        return redirect(
            "gestao_clinica:listar_medicos"
        )

    context = {
        "especialidade_choices": Especialidade.choices,
        "turno_choices": Turno.choices,
        "dia_choices": DiaSemana.choices,
        "exame_choices": TipoExame.choices,
    }

    return render(
        request,
        "gestao/criar_medico.html",
        context
    )

@login_required
def listar_medicos(request):

    medicos = Medico.objects.select_related("user").all()

    especialidade = request.GET.get("especialidade")
    status = request.GET.get("status")
    busca = request.GET.get("busca")

    if especialidade:
        medicos = medicos.filter(
            especialidade=especialidade
        )

    if status == "ativo":
        medicos = medicos.filter(ativo=True)

    elif status == "inativo":
        medicos = medicos.filter(ativo=False)

    if busca:
        medicos = medicos.filter(
            Q(user__first_name__icontains=busca) |
            Q(user__last_name__icontains=busca) |
            Q(crm__icontains=busca)
        )

    medicos = medicos.order_by("user__first_name")

    paginator = Paginator(medicos, 20)
    page = request.GET.get("page")
    medicos_pag = paginator.get_page(page)

    context = {
        "medicos": medicos_pag,
        "especialidade_choices": Especialidade.choices,
        "filtros": {
            "especialidade": especialidade or "",
            "status": status or "",
            "busca": busca or "",
        },
    }

    return render(
        request,
        "gestao/listar_medicos.html",
        context
    )


@login_required
def atualizar_medico(request, medico_id):

    medico = get_object_or_404(
        Medico.objects.select_related('user'),
        id=medico_id
    )

    if request.method == 'POST':

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        idade = request.POST.get('idade')
        crm = request.POST.get('crm')
        cpf = request.POST.get('cpf')
        especialidade = request.POST.get('especialidade')

        dias = request.POST.getlist('dias')
        turnos = request.POST.getlist('turnos')

        if not all([
            nome,
            email,
            idade,
            crm,
            cpf,
            especialidade
        ]):
            messages.error(
                request,
                'Preencha todos os campos obrigatórios.'
            )
            return redirect(
                'gestao_clinica:editar_medico',
                medico_id=medico.id
            )

        if not dias:
            messages.error(
                request,
                'Selecione pelo menos um dia de atendimento.'
            )
            return redirect(
                'gestao_clinica:editar_medico',
                medico_id=medico.id
            )

        if not turnos:
            messages.error(
                request,
                'Selecione pelo menos um turno de atendimento.'
            )
            return redirect(
                'gestao_clinica:editar_medico',
                medico_id=medico.id
            )

        # Atualiza User
        medico.user.email = email
        medico.user.save()

        # Atualiza Médico
        medico.nome = nome
        medico.idade = idade
        medico.crm = crm
        medico.cpf = cpf
        medico.especialidade = especialidade
        medico.save()

        # Remove os horários antigos
        HorarioMedico.objects.filter(
            medico=medico
        ).delete()

        # Cria novamente as combinações escolhidas
        for dia in dias:
            for turno in turnos:

                HorarioMedico.objects.create(
                    medico=medico,
                    dia=dia,
                    turno=turno
                )

        messages.success(
            request,
            'Dados do médico atualizados com sucesso.'
        )

        return redirect(
            'gestao_clinica:listar_medicos'
        )

    # Horários atuais do médico
    horarios = HorarioMedico.objects.filter(
        medico=medico
    )

    dias_medico = horarios.values_list(
        'dia',
        flat=True
    ).distinct()

    turnos_medico = horarios.values_list(
        'turno',
        flat=True
    ).distinct()

    context = {
        'medico': medico,

        'especialidade_choices': Especialidade.choices,

        'dia_choices': DiaSemana.choices,

        'turno_choices': Turno.choices,

        'dias_medico': list(dias_medico),

        'turnos_medico': list(turnos_medico),
    }

    return render(
        request,
        'gestao/atualizar_medico.html',
        context
    )

@login_required
def excluir_medico(request, medico_id):
    if not request.user.is_authenticated:
        return redirect("gestao_clinica:login_gestor")

    if not request.user.gestor.is_chefe:
        return HttpResponseForbidden("Acesso negado.")

    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == "POST":
        user = medico.user
        medico.delete()
        user.delete()

        return redirect("gestao_clinica:dashbord")

    return redirect("gestao_clinica:listar_medicos")

# MUDAR O CODIGO
@login_required
def alternar_status_medico(request, medico_id):
    """
    Ativa/inativa o médico (soft delete) em vez de excluir de verdade,
    pra não perder o histórico de Consulta/Exames/Receitas ligados a ele.
    """
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        medico.ativo = not medico.ativo
        medico.save()

        status_texto = 'ativado' if medico.ativo else 'inativado'
        messages.success(request, f'Médico {status_texto} com sucesso.')
        return redirect('gestao_clinica:listar_medicos')

    context = {'medico': medico}
    return render(request, 'gestao_clinica/confirmar_status_medico.html', context)

@login_required
def gerenciar_atendimentos(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    consultas = Consulta.objects.filter(paciente=paciente)
    exames = Exame.objects.filter(paciente=paciente)

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        atendimento_id = request.POST.get("atendimento_id")
        novo_status = request.POST.get("status")

        if tipo == "consulta":
            consulta = get_object_or_404(
                Consulta,
                id=atendimento_id,
                paciente=paciente
            )

            consulta.status = novo_status
            consulta.save()

            messages.success(
                request,
                "Status da consulta atualizado com sucesso."
            )

        elif tipo == "exame":
            exame = get_object_or_404(
                Exame,
                id=atendimento_id,
                paciente=paciente
            )

            exame.status = novo_status

            data_conclusao = request.POST.get("data_conclusao")

            if data_conclusao:
                exame.data_conclusao = data_conclusao

            exame.save()

            messages.success(
                request,
                "Exame atualizado com sucesso."
            )

        return redirect(
            "gerenciar_atendimentos",
            paciente_id=paciente.id
        )

    return render(
        request,
        "core/gerenciar_atendimentos.html",
        {
            "paciente": paciente,
            "consultas": consultas,
            "exames": exames,
            "hoje": date.today(),
        }
    )



# ---------- HISTORICOS ----------
@login_required
def registros(request):

    consultas = (
    Consulta.objects
    .select_related('paciente', 'medico')
    .order_by('-data')
)

    exames = (
    Exame.objects
    .select_related('paciente', 'medico')
    .order_by('-data')
)

    context = {
    'consultas': consultas,
    'exames': exames,
}

    return render(
    request,
    'gestao/registros.html',
    context
)

@login_required
def alterar_status_consulta(request, consulta_id):

    consulta = get_object_or_404(
        Consulta,
        id=consulta_id
    )

    if request.method == 'POST':

        consulta.status = request.POST.get('status')
        consulta.save()

        return redirect('gestao_clinica:registros')

    context = {
        'registro': consulta,
        'status_choices': Status.choices,
    }

    return render(
        request,
        'gestao/alterar_status.html',
        context
    )

@login_required
def alterar_status_exame(request, exame_id):

    exame = get_object_or_404(
        Exame,
        id=exame_id
    )

    if request.method == 'POST':

        exame.status = request.POST.get('status')
        exame.save()

        return redirect('gestao_clinica:registros')

    context = {
        'registro': exame,
        'status_choices': Status.choices,
    }

    return render(
        request,
        'gestao/alterar_status.html',
        context
    )


    
# ---------- CONFIGURAÇÃO DE VAGAS/TURNO ----------
@login_required
def vagas_disponiveis(request):

    configuracoes = (
        HorarioMedico.objects
        .select_related("medico")
        .order_by(
            "dia",
            "turno",
            "tipo_consulta",
            "tipo_exame"
        )
    )

    return render(
        request,
        "gestao/listar_configuracao_vagas.html",
        {
            "configuracoes": configuracoes
        }
    )


@login_required
def criar_vagas(request):

    medicos = Medico.objects.filter(
        ativo=True
    )

    if request.method == "POST":

        medico_id = request.POST.get("medico")
        tipo_atendimento = request.POST.get("tipo_atendimento")

        tipo_consulta = request.POST.get("tipo_consulta")
        tipo_exame = request.POST.get("tipo_exame")

        dia = request.POST.get("dia")
        turno = request.POST.get("turno")
        quantidade_vagas = request.POST.get("quantidade_vagas")

        medico = get_object_or_404(
            Medico,
            id=medico_id,
            ativo=True
        )

        # -----------------------------------------
        # VALIDAÇÃO DO TIPO
        # -----------------------------------------

        if tipo_atendimento not in ["consulta", "exame"]:

            messages.error(
                request,
                "Selecione se a configuração é para consulta ou exame."
            )

            return redirect(
                "gestao_clinica:criar_configuracao_vagas"
            )

        # -----------------------------------------
        # CONSULTA
        # -----------------------------------------

        if tipo_atendimento == "consulta":

            if not tipo_consulta:

                messages.error(
                    request,
                    "Selecione o tipo de consulta."
                )

                return redirect(
                    "gestao_clinica:criar_configuracao_vagas"
                )

            tipo_exame = None

            # A especialidade vem do médico
            especialidade = medico.especialidade

        # -----------------------------------------
        # EXAME
        # -----------------------------------------

        else:

            if not tipo_exame:

                messages.error(
                    request,
                    "Selecione o tipo de exame."
                )

                return redirect(
                    "gestao_clinica:criar_configuracao_vagas"
                )

            tipo_consulta = None

            # A especialidade vem do médico
            especialidade = medico.especialidade

        # -----------------------------------------
        # CRIA CONFIGURAÇÃO
        # -----------------------------------------

        HorarioMedico.objects.create(
            medico=medico,
            especialidade=especialidade,
            tipo_consulta=tipo_consulta,
            tipo_exame=tipo_exame,
            dia=dia,
            turno=turno,
            quantidade_vagas=quantidade_vagas
        )

        messages.success(
            request,
            "Configuração de vagas criada com sucesso."
        )

        return redirect(
            "gestao_clinica:listar_configuracao_vagas"
        )

    context = {
        "medicos": medicos,

        "tipo_consulta_choices":
            TipoConsulta.choices,

        "tipo_exame_choices":
            TipoExame.choices,

        "dia_choices":
            DiaSemana.choices,

        "turno_choices":
            Turno.choices,
    }

    return render(
        request,
        "gestao/form_configuracao_vagas.html",
        context
    )

@login_required
def atualizar_vagas_disponivies(request, config_id):

    configuracao = get_object_or_404(
        HorarioMedico,
        id=config_id
    )

    medicos = Medico.objects.filter(
        ativo=True
    )

    if request.method == "POST":

        medico_id = request.POST.get("medico")
        tipo_atendimento = request.POST.get("tipo_atendimento")

        tipo_consulta = request.POST.get("tipo_consulta")
        tipo_exame = request.POST.get("tipo_exame")

        dia = request.POST.get("dia")
        turno = request.POST.get("turno")
        quantidade_vagas = request.POST.get("quantidade_vagas")

        medico = get_object_or_404(
            Medico,
            id=medico_id,
            ativo=True
        )

        # -----------------------------------------
        # VALIDAÇÃO DO TIPO
        # -----------------------------------------

        if tipo_atendimento not in ["consulta", "exame"]:

            messages.error(
                request,
                "Selecione se a configuração é para consulta ou exame."
            )

            return redirect(
                "gestao_clinica:atualizar_configuracao_vagas",
                config_id=config_id
            )

        # -----------------------------------------
        # CONSULTA
        # -----------------------------------------

        if tipo_atendimento == "consulta":

            if not tipo_consulta:

                messages.error(
                    request,
                    "Selecione o tipo de consulta."
                )

                return redirect(
                    "gestao_clinica:atualizar_configuracao_vagas",
                    config_id=config_id
                )

            tipo_exame = None

        # -----------------------------------------
        # EXAME
        # -----------------------------------------

        else:

            if not tipo_exame:

                messages.error(
                    request,
                    "Selecione o tipo de exame."
                )

                return redirect(
                    "gestao_clinica:atualizar_configuracao_vagas",
                    config_id=config_id
                )

            tipo_consulta = None

        # -----------------------------------------
        # ESPECIALIDADE VEM DO MÉDICO
        # -----------------------------------------

        configuracao.medico = medico
        configuracao.especialidade = medico.especialidade

        configuracao.tipo_consulta = tipo_consulta
        configuracao.tipo_exame = tipo_exame

        configuracao.dia = dia
        configuracao.turno = turno
        configuracao.quantidade_vagas = quantidade_vagas

        configuracao.save()

        messages.success(
            request,
            "Configuração atualizada com sucesso."
        )

        return redirect(
            "gestao_clinica:listar_configuracao_vagas"
        )

    # Descobre qual tipo está configurado
    if configuracao.tipo_consulta:
        tipo_atendimento = "consulta"
    elif configuracao.tipo_exame:
        tipo_atendimento = "exame"
    else:
        tipo_atendimento = ""

    context = {
        "configuracao": configuracao,

        "medicos": medicos,

        "tipo_atendimento": tipo_atendimento,

        "tipo_consulta_choices": TipoConsulta.choices,

        "tipo_exame_choices": TipoExame.choices,

        "turno_choices": Turno.choices,

        "dia_choices": DiaSemana.choices,
    }

    return render(
        request,
        "gestao/form_configuracao_vagas.html",
        context
    )

@login_required
def excluir_vagas_disponivies(request, config_id):

    configuracao = get_object_or_404(
        HorarioMedico,
        id=config_id
    )

    if request.method == 'POST':

        configuracao.delete()

        messages.success(
            request,
            'Configuração removida com sucesso.'
        )

        return redirect(
            'gestao_clinica:listar_configuracao_vagas'
        )

    return render(
        request,
        'gestao/confirmar_exclusao.html',
        {
            'configuracao': configuracao
        }
    )
@login_required
def listar_medicos(request):

    medicos = Medico.objects.select_related("user").all()

    context = {
        "medicos": medicos,
    }

    return render(
        request,
        "gestao/listar_medico.html",
        context
    )


@login_required
def listar_gestores(request):

    # Somente o gestor chefe pode visualizar os gestores
    if not request.user.gestor.is_chefe:
        return HttpResponseForbidden("Acesso negado.")

    gestores = Gestor.objects.select_related("user").all()

    context = {
        "gestores": gestores,
    }

    return render(
        request,
        "gestao/listar_gestores.html",
        context
    )


@login_required
def detalhe_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)

    return render(
        request,
        "gestao/detalhe_gestor.html",
        {
            "gestor": gestor,
        }
    )


@login_required
def detalhe_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    return render(
        request,
        "gestao/detalhe_medico.html",
        {
            "medico": medico,
        }
    )

def pacientes(request):

    pacientes_lista = Paciente.objects.all().order_by('nome')

    paginator = Paginator(pacientes_lista, 10)

    page_number = request.GET.get('page')

    pacientes = paginator.get_page(page_number)

    return render(
        request,
        'gestao/pacientes.html',
        {
            'pacientes': pacientes
        }
    )