from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pqr.models import Queja

# -------------------
# Dashboards por rol
# -------------------
@login_required
def dashboard_ciudadano(request):
    quejas = Queja.objects.filter(ciudadano__usuario=request.user).order_by('-fecha_reporte')

    total_abiertas = quejas.count()
    total_en_proceso = quejas.filter(estado__nombre="En Proceso").count()
    total_cerradas = quejas.filter(estado__nombre="Cerrada").count()

    return render(request, 'dashboard/dashboard_ciudadano.html', {
        'quejas': quejas,
        'total_abiertas': total_abiertas,
        'total_en_proceso': total_en_proceso,
        'total_cerradas': total_cerradas,
    })


@login_required
def dashboard_tecnico(request):
    quejas = Queja.objects.filter(tecnico__usuario=request.user).order_by('-fecha_reporte')
    return render(request, 'dashboard/dashboard_tecnico.html', {'quejas': quejas})


@login_required
def dashboard_admin(request):
    quejas = Queja.objects.all().order_by('-fecha_reporte')
    return render(request, 'dashboard/dashboard_admin.html', {'quejas': quejas})
