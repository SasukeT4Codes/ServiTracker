from django.shortcuts import render

def index(request):
  return render(request, 'index.html')

def servicios(request):
  return render(request, 'servicios.html')

def nosotros(request):
  return render(request, 'nosotros.html')

def contacto(request):
  return render(request, 'contacto.html')

