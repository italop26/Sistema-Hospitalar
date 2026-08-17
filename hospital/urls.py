
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path('', include('pacientes.urls')),
    path('gestao/', include('gestao_clinica.urls'))
]
