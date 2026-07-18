from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Paciente, Consulta, Exame, StatusExame
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator



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
    return render(request, 'login.html')
        

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
        )
        if paciente:
            return render(request, 'login.html')
        return HttpResponse("Erro ao criar conta")
    return render(request, 'criar_conta.html')

def principal(request):
    paciente = request.user.paciente if request.user.is_authenticated else None
    consultas = Consulta.objects.filter(paciente=paciente)
    exames = Exame.objects.filter(paciente=paciente)
    
    return render(request, 'principal.html', {'paciente': paciente, 'consultas': consultas, 'exames': exames})

def marcacao(request):
    paciente = request.user.paciente
    tipo = request.GET.get("tipo", "consulta")

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        if tipo == "consulta":
            Consulta.objects.create(
                paciente=paciente,
                especialidade=request.POST.get("especialidade"),
                data_consulta=request.POST.get("data_consulta"),
            )

        elif tipo == "exame":
            Exame.objects.create(
                paciente=paciente,
                tipo_exame=request.POST.get("tipo_exame"),
                data_exame=request.POST.get("data_exame"),
                descricao=request.POST.get("descricao")
            )

        return redirect("principal")

    return render(request, "marcacao.html", {
        "tipo": tipo
    })
            
        

def perfil(request):
    if request.user.is_authenticated:

        paciente = request.user.paciente
        return render(request, 'perfil.html', {'paciente': paciente})
        
           
    else:
        return HttpResponse('Erro')

def ver_exames(request):
    paciente = request.user.paciente
    exames = Exame.objects.filter(paciente=paciente)
    paginator = Paginator(exames, 10)
    page = request.GET.get("page")

    exames = paginator.get_page(page)
    return render(request, 'ver_exames.html', {'exames': exames})

def ver_consultas(request):
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente)
    paginator = Paginator(consultas, 10)
    page = request.GET.get("page")

    exames = paginator.get_page(page)
    return render(request, 'ver_consultas.html', {'consultas': consultas})

def sair(request):
    logout(request)
    return redirect('login')
    

    
