from django.shortcuts import render

# -------------------
# Vistas públicas
# -------------------
def index(request):
    return render(request, 'portal/index.html')

def servicios(request):
    return render(request, 'portal/servicios.html')

def nosotros(request):
    return render(request, 'portal/nosotros.html')

def contacto(request):
    return render(request, 'portal/contacto.html')

def saludo(request):
    return render(request, 'portal/saludo.html')
