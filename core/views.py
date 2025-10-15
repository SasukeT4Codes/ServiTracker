from django.shortcuts import render

def index(request):
    context = {'name': 'Estudiante UDI'}
    return render(request, 'index.html', context)

def saludo(request):
    nombre = request.GET.get('nombre')
    edad = request.GET.get('edad')

    context = {
        'nombre': nombre,
        'edad': edad,
        'has_data': bool(nombre and edad)
    }
    return render(request, 'saludo.html', context)
