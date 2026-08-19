from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from gestao_clinica import choices
from gestao_clinica.especialidades import Especialidade
from .models import ConfiguracaoVagas
from .models import Gestor
from gestao_clinica.turnos import Turno
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

    # Período do dashboard
    data_inicial = hoje - timedelta(days=5)
    data_final = hoje + timedelta(days=4)

    consultas = (
        Consulta.objects
        .filter(data__range=(data_inicial, data_final))
        .select_related("paciente")
        .order_by("data")
    )

    exames = (
        Exame.objects
        .filter(data__range=(data_inicial, data_final))
        .select_related("paciente")
        .order_by("data")
    )

    # Quantidades
    consultas_de_hoje = Consulta.objects.filter(data=hoje).count()
    exames_de_hoje = Exame.objects.filter(data=hoje).count()
    total_medicos = Medico.objects.count()
    total_pacientes = Paciente.objects.count()

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
            "total": len(consultas_do_dia) + len(exames_do_dia),
        })

        data_atual += timedelta(days=1)

    context = {
        "dias": dias,
        "data_inicial": data_inicial,
        "data_final": data_final,
        "hoje": hoje,

        "pacientes": total_pacientes,
        "medicos": total_medicos,

        "consultas_de_hoje": consultas_de_hoje,
        "exames_de_hoje": exames_de_hoje,
    }

    return render(
        request,
        "gestao/dashbord.html",
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
def criar_medico(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        idade = request.POST.get('idade')
        crm = request.POST.get('crm')
        cpf = request.POST.get('cpf')
        especialidade = request.POST.get('especialidade')

        if not all([first_name, username, idade, crm, cpf, especialidade]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('gestao_clinica:criar_medico')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Já existe um usuário com esse username.')
            return redirect('gestao_clinica:criar_medico')

        if Medico.objects.filter(crm=crm).exists():
            messages.error(request, 'Já existe um médico com esse CRM.')
            return redirect('gestao_clinica:criar_medico')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        Medico.objects.create(
            user=user,
            idade=idade,
            crm=crm,
            cpf=cpf,
            especialidade=especialidade,
        )

        messages.success(request, f'Médico {first_name} cadastrado com sucesso.')
        return redirect('gestao_clinica:listar_medicos')

    context = {'especialidade_choices': Especialidade.choices}
    return render(request, 'gestao/criar_medico.html', context)


@login_required
def atualizar_medico(request, medico_id):
    medico = get_object_or_404(Medico.objects.select_related('user'), id=medico_id)

    if request.method == 'POST':
        medico.user.first_name = request.POST.get('first_name', medico.user.first_name)
        medico.user.last_name = request.POST.get('last_name', medico.user.last_name)
        medico.user.email = request.POST.get('email', medico.user.email)
        medico.user.save()

        medico.idade = request.POST.get('idade', medico.idade)
        medico.crm = request.POST.get('crm', medico.crm)
        medico.cpf = request.POST.get('cpf', medico.cpf)
        medico.especialidade = request.POST.get('especialidade', medico.especialidade)
        medico.save()

        messages.success(request, 'Dados do médico atualizados.')
        return redirect('gestao_clinica:listar_medicos')

    context = {
        'medico': medico,
        'especialidade_choices': Especialidade.choices,
    }
    return render(request, 'gestao_clinica/listar_medicos.html', context)

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



# ---------- CONFIGURAÇÃO DE VAGAS/TURNO ----------
@login_required
def registros(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente).order_by('-data')
    exames = Exame.objects.filter(paciente=paciente).order_by('-data')

    context = {'consultas': consultas, 'exames': exames}
    return render (request, 'gestao/registros.html', context)

    

@login_required
def vagas_disponiveis(request):
    configuracoes = ConfiguracaoVagas.objects.all().order_by('especialidade', 'turno')
    context = {'configuracoes': configuracoes}
    return render(request, 'gestao/listar_configuracao_vagas.html', context)


@login_required
def criar_vagas(request):
    if request.method == 'POST':
        especialidade = request.POST.get('especialidade')
        turno = request.POST.get('turno')
        quantidade = request.POST.get('quantidade_vagas')

        if not (especialidade and turno and quantidade):
            messages.error(request, 'Preencha todos os campos.')
            return redirect('gestao:criar_configuracao_vagas')

        if ConfiguracaoVagas.objects.filter(especialidade=especialidade, turno=turno).exists():
            messages.error(request, 'Já existe configuração para essa especialidade e turno.')
            return redirect('gestao:criar_configuracao_vagas')

        ConfiguracaoVagas.objects.create(
            especialidade=especialidade,
            turno=turno,
            quantidade_vagas=quantidade
        )
        messages.success(request, 'Configuração de vagas criada com sucesso.')
        return redirect('gestao:listar_configuracao_vagas')

    context = {
        'especialidade_choices': Especialidade.choices,
        'turno_choices': Turno.choices,
    }
    return render(request, 'gestao/form_configuracao_vagas.html', context)


@login_required
def atualizar_vagas_disponivies(request, config_id):
    configuracao = get_object_or_404(ConfiguracaoVagas, id=config_id)

    if request.method == 'POST':
        quantidade = request.POST.get('quantidade_vagas')

        if not quantidade:
            messages.error(request, 'Informe a quantidade de vagas.')
            return redirect('gestao:atualizar_configuracao_vagas', config_id=config_id)

        configuracao.quantidade_vagas = quantidade
        configuracao.save()
        messages.success(request, 'Quantidade de vagas atualizada.')
        return redirect('gestao:listar_configuracao_vagas')

    context = {'configuracao': configuracao}
    return render(request, 'gestao/form_configuracao_vagas.html', context)


@login_required
def excluir_vagas_disponivies(request, config_id):
    configuracao = get_object_or_404(ConfiguracaoVagas, id=config_id)

    if request.method == 'POST':
        configuracao.delete()
        messages.success(request, 'Configuração removida.')
        return redirect('gestao:listar_configuracao_vagas')

    context = {'configuracao': configuracao}
    return render(request, 'gestao/confirmar_exclusao.html', context)

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