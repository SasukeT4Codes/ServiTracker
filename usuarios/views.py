from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Ciudadano
from .forms import UsuarioForm
from pqr.models import Ubicacion

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
        form = UsuarioForm(request.POST, crear=True)
        if form.is_valid():
            usuario = form.save()

            # Si es ciudadano, crear perfil y dirección inicial
            if usuario.rol == Usuario.Rol.CIUDADANO:
                ciudadano = Ciudadano.objects.create(usuario=usuario)
                direccion = form.cleaned_data.get('direccion_inicial')
                if direccion:
                    Ubicacion.objects.create(
                        ciudadano=ciudadano,
                        direccion=direccion
                    )

            messages.success(request, "Usuario creado correctamente.")
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm(crear=True)

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
        # importante: pasar crear=False para que el form sepa que es edición
        form = UsuarioForm(request.POST, instance=usuario, crear=False)
        if form.is_valid():
            usuario = form.save()

            # Si ahora es ciudadano y no tenía perfil, crearlo
            if usuario.rol == Usuario.Rol.CIUDADANO:
                ciudadano, created = Ciudadano.objects.get_or_create(usuario=usuario)
                direccion = form.cleaned_data.get('direccion_inicial')
                # Si se ingresó dirección y no tenía ninguna, crearla
                if direccion and not ciudadano.direcciones.exists():
                    Ubicacion.objects.create(
                        ciudadano=ciudadano,
                        direccion=direccion
                    )

            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('admin_gestion_usuarios')
    else:
        form = UsuarioForm(instance=usuario, crear=False)

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
