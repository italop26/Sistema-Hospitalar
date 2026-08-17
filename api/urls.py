from django.urls import path

from .views import ConsultaAPIView, ExameAPIView


urlpatterns = [

    path(
        "consultas/",
        ConsultaAPIView.as_view(),
        name="api-consultas"
    ),

    path(
        "exames/",
        ExameAPIView.as_view(),
        name="api-exames"
    ),

]