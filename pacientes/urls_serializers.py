from django.urls import path
from . import views_serializers

urlpatterns = [
    # Autenticação
    path('login/', views_serializers.login_api, name='login_api'),
    path('criar-conta/', views_serializers.criar_conta, name='criar_conta_api'),

    # Paciente
    path('perfil/', views_serializers.perfil_api, name='perfil_api'),
    path('principal/', views_serializers.principal_api, name='principal_api'),

    # Consultas
    path('marcacao/', views_serializers.marcacao_api, name='agendamento_de_consulta'),
    
 
]