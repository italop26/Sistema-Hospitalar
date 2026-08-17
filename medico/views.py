from django.shortcuts import render
from models import Medico

def perfil(request):
    perfil = Medico.objects.all()
    return render(request, 'perfil.html', {'perfil': perfil})

