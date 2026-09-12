from django.urls import path
from . import views

app_name = 'gestao_clinica'

urlpatterns = [

    # =========================
    # LOGIN / DASHBOARD
    # =========================

    path(
        '',
        views.login_gestor,
        name='login_gestor'
    ),
    path(
    "logout/",
    views.logout_gestor,
    name="logout_gestor"
    ),

    path(
        'dashbord/',
        views.dashboard,
        name='dashbord'
    ),


    # =========================
    # GESTORES
    # =========================

    path(
        'gestores/criar/',
        views.criar_gestor,
        name='criar_gestor'
    ),

    path(
        'gestores/<int:id_gestor>/excluir/',
        views.excluir_gestor,
        name='excluir_gestor'
    ),


    

    # =========================
    # MÉDICOS
    # =========================

    path(
        'medicos/',
        views.listar_medicos,
        name='listar_medicos'
    ),

    path(
        'medicos/novo/',
        views.criar_medico,
        name='criar_medico'
    ),

    path(
        'medicos/<int:medico_id>/editar/',
        views.atualizar_medico,
        name='atualizar_medico'
    ),

    path(
        'medicos/<int:medico_id>/deletar/',
        views.excluir_medico,
        name='excluir_medico'
    ),

    path(
        'medicos/<int:medico_id>/status/',
        views.alternar_status_medico,
        name='alternar_status_medico'
    ),
    # =========================
    # MÉDICOS
    # =========================
        path(
        "pacientes/<int:paciente_id>/atendimentos/",
        views.gerenciar_atendimentos,
        name="gerenciar_atendimentos",
    ),

    path(
        "pacientes/<int:paciente_id>/registros/",
        views.registros,
        name="registros",
    ),

    path(
        "vagas/",
        views.vagas_disponiveis,
        name="listar_configuracao_vagas",
    ),

    path(
        "vagas/criar/",
        views.criar_vagas,
        name="criar_configuracao_vagas",
    ),

    path(
        "vagas/<int:config_id>/editar/",
        views.atualizar_vagas_disponivies,
        name="atualizar_configuracao_vagas",
    ),

    path(
        "vagas/<int:config_id>/excluir/",
        views.excluir_vagas_disponivies,
        name="excluir_configuracao_vagas",
    ),

     # Médicos
    path(
        "medicos/",
        views.listar_medicos,
        name="listar_medicos"
    ),

    # Gestores
    path(
        "gestores/",
        views.listar_gestores,
        name="listar_gestores"
    ),

    #Detalhes
    path('detalhe_gestor/<int:gestor_id>/', views.detalhe_gestor, name='detalhe_gestor'),
    path('detalhe_medico/<int:medico_id>/', views.detalhe_medico, name='detalhe_medico'),

    path(
        'pacientes/',
        views.pacientes,
        name='pacientes'
    ),

    path('registros_salvos/', views.registros, name='registros'),

    path(
    'consultas/<int:consulta_id>/status/',
    views.alterar_status_consulta,
    name='alterar_status_consulta'
    ),

    path(
    'exames/<int:exame_id>/status/',
    views.alterar_status_exame,
    name='alterar_status_exame'
    ),
]