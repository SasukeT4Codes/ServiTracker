from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm  # asegúrate de tener este form definido

# -------------------
# Listar usuarios
# -------------------
@login_required
def admin_gestion_usuarios(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')  # seguridad

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/admin_gestion_usuarios.html', {
        'usuarios': usuarios
    })


# -------------------
# Crear usuario
# -------------------
@login_required
def admin_crear_usuario(request):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/admin_usuario_form.html', {
        'form': form,
        'accion': 'Crear'
    })


# -------------------
# Editar usuario
# -------------------
@login_required
def admin_editar_usuario(request, usuario_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/admin_usuario_form.html', {
        'form': form,
        'accion': 'Editar'
    })


# -------------------
# Eliminar usuario
# -------------------
@login_required
def admin_eliminar_usuario(request, usuario_id):
    if request.user.rol != 'administrativo' and not request.user.is_superuser:
        return redirect('dashboard_admin')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('admin_gestion_usuarios')

    return render(request, 'usuarios/admin_usuario_confirm_delete.html', {
        'usuario': usuario
    })


# -------------------
# Redirección dinámica después de login
# -------------------
@login_required
def redireccion_dashboard(request):
    user = request.user
    if user.rol == 'ciudadano':
        return redirect('dashboard_ciudadano')
    elif user.rol == 'tecnico':
        return redirect('dashboard_tecnico')
    elif user.rol == 'administrativo' or user.is_superuser:
        return redirect('dashboard_admin')
    else:
        return redirect('index')  # fallback
