from django.shortcuts import render

def index(request):
    context = {'name': 'Estudiante UDI'}
    return render(request, 'index.html', context)
