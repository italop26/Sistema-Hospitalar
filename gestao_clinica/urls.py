from django.urls import path
from . import views

app_name = 'gestao_clinica'

urlpatterns = [
    path('', views.login_gestor, name='login_gestor'),
    path('dashbord/', views.dashboard, name='dashbord'),

    #Manipulação dos gestores
    path('criar_gestor', views.criar_gestor, name='criar_gestor'),
    path('excluir/<int:id_gestor>/', views.excluir_gestor, name='excluir_gestor'),

    #Atendimentos
    path('atendimentos/', views.listar_atendimentos, name='listar_atendimentos'),
    #Vagas 
    path('vagas/', views.listar_configuracao_vagas, name='listar_configuracao_vagas'),
    path('vagas/nova/', views.criar_configuracao_vagas, name='criar_configuracao_vagas'),
    path('vagas/<int:config_id>/editar/', views.atualizar_configuracao_vagas, name='atualizar_configuracao_vagas'),
    path('vagas/<int:config_id>/excluir/', views.excluir_configuracao_vagas, name='excluir_configuracao_vagas'),

    # gestao_clinica/urls.py (adicionar)
    path('medicos/', views.listar_medicos, name='listar_medicos'),
    path('medicos/novo/', views.criar_medico, name='criar_medico'),
    path('medicos/<int:medico_id>/editar/', views.atualizar_medico, name='atualizar_medico'),
    path('medicos/<int:medico_id>/status/', views.alternar_status_medico, name='alternar_status_medico'),
]