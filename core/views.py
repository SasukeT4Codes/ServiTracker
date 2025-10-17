from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuejaForm, ComentarioForm, CambiarEstadoForm
from .models import Queja, Ciudadano, ComentarioQueja

# -------------------
# Vistas públicas
# -------------------
def index(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request, 'servicios.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')


# -------------------
# Dashboard según rol
# -------------------
@login_required
def dashboard(request):
    if request.user.rol == 'ciudadano':
        quejas = Queja.objects.filter(ciudadano__usuario=request.user).order_by('-fecha_reporte')
        return render(request, 'dashboard_ciudadano.html', {'quejas': quejas})

    elif request.user.rol == 'tecnico':
        quejas = Queja.objects.filter(tecnico__usuario=request.user).order_by('-fecha_reporte')
        return render(request, 'dashboard_tecnico.html', {'quejas': quejas})

    elif request.user.rol == 'administrativo':
        quejas = Queja.objects.all().order_by('-fecha_reporte')
        return render(request, 'dashboard_admin.html', {'quejas': quejas})

    else:
        return redirect('index')


# -------------------
# Crear PQR (solo ciudadanos)
# -------------------
@login_required
def crear_queja(request):
    if request.user.rol != 'ciudadano':
        return redirect('dashboard')

    if request.method == 'POST':
        form = QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            queja.ciudadano = Ciudadano.objects.get(usuario=request.user)
            queja.estado_id = 1  # Estado inicial (ej. "Pendiente")
            queja.save()
            return redirect('dashboard')
    else:
        form = QuejaForm()
    return render(request, 'crear_queja.html', {'form': form})


# -------------------
# Panel de empleados (técnicos y administrativos)
# -------------------
@login_required
def panel_empleados(request):
    if request.user.rol == 'administrativo':
        quejas = Queja.objects.all().order_by('-fecha_reporte')
    elif request.user.rol == 'tecnico':
        quejas = Queja.objects.filter(tecnico__usuario=request.user).order_by('-fecha_reporte')
    else:
        return redirect('dashboard')

    return render(request, 'panel_empleados.html', {'quejas': quejas})


# -------------------
# Cambiar estado de una queja (solo administrativos)
# -------------------
@login_required
def cambiar_estado(request, queja_id):
    if request.user.rol != 'administrativo':
        return redirect('dashboard')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = CambiarEstadoForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CambiarEstadoForm(instance=queja)

    return render(request, 'cambiar_estado.html', {'form': form, 'queja': queja})


# -------------------
# Agregar comentario a una queja (técnicos y administrativos)
# -------------------
@login_required
def agregar_comentario(request, queja_id):
    queja = get_object_or_404(Queja, id=queja_id)

    if request.user.rol not in ['tecnico', 'administrativo']:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.queja = queja
            comentario.autor = request.user.username
            comentario.save()
            return redirect('dashboard')
    else:
        form = ComentarioForm()

    return render(request, 'agregar_comentario.html', {'form': form, 'queja': queja})



# Errores:

def error_404_test(request):
    return render(request, '404.html', status=404)

def error_500_test(request):
    return render(request, '500.html', status=500)