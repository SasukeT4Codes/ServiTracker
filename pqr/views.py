from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Queja, ComentarioQueja, Ubicacion
from .forms import QuejaForm, QuejaFormAdmin, ComentarioForm, CambiarEstadoForm
from usuarios.models import Ciudadano

# -------------------
# Crear PQR
# -------------------
@login_required
def crear_queja(request):
    es_admin = request.user.rol == 'administrativo' or request.user.is_superuser
    if request.user.rol not in ['ciudadano', 'administrativo'] and not request.user.is_superuser:
        return redirect('dashboard_ciudadano')

    if request.method == 'POST':
        form = QuejaFormAdmin(request.POST) if es_admin else QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            if not es_admin:
                queja.ciudadano = Ciudadano.objects.get(usuario=request.user)
            queja.estado_id = 1
            queja.save()
            return redirect('admin_panel_quejas' if es_admin else 'dashboard_ciudadano')
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
        return redirect('dashboard_ciudadano')

    return render(request, 'pqr/panel_empleados.html', {'quejas': quejas})


# -------------------
# Cambiar estado
# -------------------
@login_required
def cambiar_estado(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

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
        return redirect('dashboard_ciudadano')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.queja = queja
            comentario.autor = request.user.username
            comentario.save()
            return redirect('admin_panel_quejas' if request.user.rol in ['administrativo'] or request.user.is_superuser else 'dashboard_ciudadano')
    else:
        form = ComentarioForm()

    return render(request, 'pqr/agregar_comentario.html', {'form': form, 'queja': queja})


# -------------------
# Panel administrativo de PQR
# -------------------
from django import forms

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
        return redirect('dashboard_admin')

    quejas = Queja.objects.all().order_by('-fecha_reporte')
    return render(request, 'pqr/admin_panel_quejas.html', {'quejas': quejas})


@login_required
def admin_asignar_tecnico(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_quejas')
    else:
        form = AsignarTecnicoForm(instance=queja)

    return render(request, 'pqr/admin_asignar_tecnico.html', {'form': form, 'queja': queja})


@login_required
def admin_editar_queja(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        form = EditarQuejaForm(request.POST, instance=queja)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_quejas')
    else:
        form = EditarQuejaForm(instance=queja)

    return render(request, 'pqr/admin_editar_queja.html', {'form': form, 'queja': queja})


@login_required
def admin_eliminar_queja(request, queja_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    queja = get_object_or_404(Queja, id=queja_id)

    if request.method == 'POST':
        queja.delete()
        return redirect('admin_panel_quejas')

    return render(request, 'pqr/admin_confirm_delete_queja.html', {'queja': queja})


# -------------------
# Reportes administrativos
# -------------------
@login_required
def admin_reportes(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    total_quejas = Queja.objects.count()
    por_estado = Queja.objects.values('estado__nombre').annotate(total=Count('id'))
    por_tecnico = Queja.objects.values('tecnico__usuario__username').annotate(total=Count('id'))

    context = {
        'total_quejas': total_quejas,
        'por_estado': por_estado,
        'por_tecnico': por_tecnico,
    }
    return render(request, 'pqr/admin_reportes.html', context)
