from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('login/', views.login_view, name='login'),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    path('principal/', views.principal, name='principal'),
    path('marcacao/', views.marcacao, name='marcacao'),
    path('perfil/', views.perfil, name='perfil'),
    path('ver_exames',views.ver_exames, name='ver_exames'),
    path('ver_consultas',views.ver_consultas, name='ver_consultas'),
    path(
            "logout/",
            views.sair,
            name="logout_paciente"
        ),
    path(
        "atendimentos/",
        views.meus_atendimentos,
        name="meus_atendimentos"
    ),

    path(
        "consulta/<int:consulta_id>/",
        views.ver_atendimento_consulta,
        name="ver_atendimento_consulta"
    ),

    path(
        "exame/<int:exame_id>/",
        views.ver_resultado_exame,
        name="ver_resultado_exame"
    ),

    path(
        "receitas/",
        views.receitas,
        name="receitas"
    ),
   
]