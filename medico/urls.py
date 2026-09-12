from django.urls import path

from . import views


app_name = "medico"


urlpatterns = [

    # Login
    path(
        "",
        views.login_medico,
        name="login_medico"
    ),

    # Logout
    path(
        "logout/",
        views.logout,
        name="logout_medico"
    ),
    # Perfil
    path('perfil/', views.perfil_medico, name='perfil'),

    # Painel
    path(
        "painel/",
        views.painel_medico,
        name="painel"
    ),

    # Consultas
    path(
        "consulta/<int:consulta_id>/",
        views.iniciar_consulta,
        name="iniciar_consulta"
    ),

    path(
        "consulta/<int:consulta_id>/salvar/",
        views.salvar_atendimento_consulta,
        name="salvar_atendimento_consulta"
    ),

    path(
        "consulta/<int:consulta_id>/confirmar/",
        views.confirmar_consulta,
        name="confirmar_consulta"
    ),

    # Exames
    path(
        "exame/<int:exame_id>/",
        views.iniciar_exame,
        name="iniciar_exame"
    ),

    path(
        "exame/<int:exame_id>/salvar/",
        views.salvar_atendimento_exame,
        name="salvar_atendimento_exame"
    ),

    path(
        "exame/<int:exame_id>/confirmar/",
        views.confirmar_exame,
        name="confirmar_exame"
    ),


]