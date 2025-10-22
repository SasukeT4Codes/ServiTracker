from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django import forms
from .forms import QuejaForm, QuejaFormAdmin, ComentarioForm, CambiarEstadoForm, UsuarioForm
from .models import Queja, Ciudadano, ComentarioQueja, Ubicacion

Usuario = get_user_model()

# -------------------
# Vistas públicas (nucleo)
# -------------------
def index(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request, 'nucleo/servicios.html')

def nosotros(request):
    return render(request, 'nucleo/nosotros.html')

def contacto(request):
    return render(request, 'nucleo/contacto.html')


# -------------------
# Dashboard según rol
# -------------------
@login_required
def dashboard(request):
    if request.user.rol == 'ciudadano':
        quejas = Queja.objects.filter(ciudadano__usuario=request.user).order_by('-fecha_reporte')
        return render(request, 'dashboard/dashboard_ciudadano.html', {'quejas': quejas})

    if request.user.rol == 'tecnico':
        quejas = Queja.objects.filter(tecnico__usuario=request.user).order_by('-fecha_reporte')
        return render(request, 'dashboard/dashboard_tecnico.html', {'quejas': quejas})

    if request.user.rol == 'administrativo' or request.user.is_superuser:
        quejas = Queja.objects.all().order_by('-fecha_reporte')
        return render(request, 'dashboard/dashboard_admin.html', {'quejas': quejas})

    return redirect('index')


# -------------------
# Crear PQR (ciudadanos y administrativos)
# -------------------
@login_required
def crear_queja(request):
    if request.user.rol not in ['ciudadano', 'administrativo'] and not request.user.is_superuser:
        return redirect('dashboard')

    es_admin = request.user.rol == 'administrativo' or request.user.is_superuser

    if request.method == 'POST':
        form = QuejaFormAdmin(request.POST) if es_admin else QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            if not es_admin:
                queja.ciudadano = Ciudadano.objects.get(usuario=request.user)
            queja.estado_id = 1
            queja.save()
            return redirect('admin_panel_quejas' if es_admin else 'dashboard')
    else:
        form = QuejaFormAdmin() if es_admin else QuejaForm()

    return render(request, 'pqr/crear_queja.html', {'form': form, 'es_admin': es_admin})


# -------------------
# Panel de empleados
# -------------------
@login_required
def panel_empleados(request):
    if request.user.rol == 'administrativo':
        quejas = Queja.objects.all().order_by('-fecha_reporte')
    elif request.user.rol == 'tecnico':
        quejas = Queja.objects.filter(tecnico__usuario=request.user).order_by('-fecha_reporte')
    else:
        return redirect('dashboard')

    return render(request, 'pqr/panel_empleados.html', {'quejas': quejas})


# -------------------
# Cambiar estado de una queja
# -------------------
@login_required
def cambiar_estado(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = CambiarEstadoForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_quejas')
    else:
        form = CambiarEstadoForm(instance=queja)

    return render(request, 'pqr/cambiar_estado.html', {'form': form, 'queja': queja})


# -------------------
# Agregar comentario
# -------------------
@login_required
def agregar_comentario(request, queja_id):
    queja = get_object_or_404(Queja, id=queja_id)

    if request.user.rol not in ['tecnico', 'administrativo'] and not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.queja = queja
            comentario.autor = request.user.username
            comentario.save()
            return redirect('admin_panel_quejas' if request.user.rol in ['administrativo'] or request.user.is_superuser else 'dashboard')
    else:
        form = ComentarioForm()

    return render(request, 'pqr/agregar_comentario.html', {'form': form, 'queja': queja})


# -------------------
# Gestión de usuarios
# -------------------
@login_required
def admin_gestion_usuarios(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'dashboard/admin_gestion_usuarios.html', {'usuarios': usuarios})


@login_required
def admin_crear_usuario(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, crear=True)   # flag crear=True
        if form.is_valid():
            usuario = form.save()
            # Si es ciudadano, crear perfil y dirección inicial
            if usuario.rol == Usuario.Rol.CIUDADANO:
                ciudadano, _ = Ciudadano.objects.get_or_create(usuario=usuario)
                direccion_inicial = form.cleaned_data.get('direccion_inicial')
                if direccion_inicial:
                    Ubicacion.objects.create(
                        ciudadano=ciudadano,
                        direccion=direccion_inicial
                    )
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm(crear=True)   # ← flag crear=True

    return render(request, 'dashboard/admin_usuario_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def admin_editar_usuario(request, usuario_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)  # sin flag, edición
        if form.is_valid():
            usuario = form.save()
            # Si se cambia a ciudadano y no tiene perfil, crearlo
            if usuario.rol == Usuario.Rol.CIUDADANO:
                ciudadano, _ = Ciudadano.objects.get_or_create(usuario=usuario)
                direccion_inicial = form.cleaned_data.get('direccion_inicial')
                if direccion_inicial and not ciudadano.direcciones.exists():
                    Ubicacion.objects.create(
                        ciudadano=ciudadano,
                        direccion=direccion_inicial
                    )
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm(instance=usuario)  # sin flag, edición

    return render(request, 'dashboard/admin_usuario_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def admin_eliminar_usuario(request, usuario_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('admin_gestion_usuarios')

    return render(request, 'dashboard/admin_usuario_confirm_delete.html', {'usuario': usuario})


# -------------------
# Panel administrativo de PQR con acciones
# -------------------
class AsignarTecnicoForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['tecnico']

class EditarQuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['direccion', 'tipo_falla', 'descripcion', 'tecnico', 'estado']
        widgets = {
            'direccion': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'direccion': 'Dirección',
            'tipo_falla': 'Tipo de falla',
            'descripcion': 'Descripción',
            'tecnico': 'Técnico asignado',
            'estado': 'Estado',
        }


@login_required
def admin_panel_quejas(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    quejas = Queja.objects.all().order_by('-fecha_reporte')
    return render(request, 'dashboard/admin_panel_quejas.html', {'quejas': quejas})


@login_required
def admin_asignar_tecnico(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_quejas')
    else:
        form = AsignarTecnicoForm(instance=queja)

    return render(request, 'dashboard/admin_asignar_tecnico.html', {'form': form, 'queja': queja})


@login_required
def admin_editar_queja(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = EditarQuejaForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_quejas')
    else:
        form = EditarQuejaForm(instance=queja)

    return render(request, 'dashboard/admin_editar_queja.html', {'form': form, 'queja': queja})


@login_required
def admin_eliminar_queja(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        queja.delete()
        return redirect('admin_panel_quejas')

    return render(request, 'dashboard/admin_confirm_delete_queja.html', {'queja': queja})


# -------------------
# Reportes administrativos (solo administrativos)
# -------------------
@login_required
def admin_reportes(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard')

    total_quejas = Queja.objects.count()
    por_estado = Queja.objects.values('estado__nombre').annotate(total=Count('id'))
    por_tecnico = Queja.objects.values('tecnico__usuario__username').annotate(total=Count('id'))

    context = {
        'total_quejas': total_quejas,
        'por_estado': por_estado,
        'por_tecnico': por_tecnico,
    }
    return render(request, 'dashboard/admin_reportes.html', context)


# -------------------
# Errores de prueba
# -------------------
def error_404_test(request):
    return render(request, '404.html', status=404)

def error_500_test(request):
    return render(request, '500.html', status=500)
