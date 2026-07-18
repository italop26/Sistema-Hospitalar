from rest_framework import viewsets, status
from .models import Paciente, Exame, Consulta, StatusExame
from .serializers import PacienteSerializer, ExameSerializer, ConsultaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@api_view(['POST'])
def login_api(request):
    cpf = request.data.get('cpf')
    password = request.data.get('senha')
    user = authenticate(username=cpf, password=password)
    if user is not None:            
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
             'access' : str(access),
             'refresh': str(refresh)
            })
    else:
        return Response(
                  {"erro": "Usuário ou senha inválidos."},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
def criar_conta(request):
      
    user = User.objects.create_user(
        username=request.data.get('cpf'),
        password=request.data.get('senha')
    )

    
    paciente = Paciente.objects.create(
        user=user,
        nome=request.data.get('nome'),
        idade=request.data.get('idade'),
        email=request.data.get('email'),
        telefone=request.data.get('telefone'),
        data_nascimento=request.data.get('data_nascimento'),
        cpf=request.data.get('cpf')
    )

    
    serializer = PacienteSerializer(paciente)

    
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def principal_api(request):
    paciente = request.user.paciente if request.user.is_authenticated else None

    consultas = Consulta.objects.filter(paciente=paciente)

    serializer = ConsultaSerializer(consultas, many=True)

    return Response(serializer.data)

@api_view(["POST"])
def marcacao_api(request):

    paciente = request.user.paciente
    tipo = request.data.get("tipo")

    if tipo == "consulta":
        serializer = ConsultaSerializer(data=request.data)

    elif tipo == "exame":
        serializer = ExameSerializer(data=request.data)

    else:
        return Response(
            {"erro": "Tipo inválido."},
            status=400
        )

    if serializer.is_valid():
        serializer.save(paciente=paciente)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)



@api_view(['GET'])
def perfil_api(request):
    paciente = request.user.paciente
    if request.user.is_authenticated:
        paciente = request.user.paciente
    
    else:
        return HttpResponse()
    
    serializer = PacienteSerializer(paciente)
    return Response(serializer.data)



