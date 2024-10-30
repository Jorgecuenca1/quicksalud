from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from .models import Servicio, SubServicio, Direccion, Medico, Historial
from django.shortcuts import get_object_or_404
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import SolicitudServicio, Historial, Medico
from django.contrib.auth.decorators import login_required

@login_required
def ver_solicitudes(request):
    medico = Medico.objects.get(user=request.user)
    solicitudes = SolicitudServicio.objects.filter(medico=medico, estado='pendiente')
    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def responder_solicitud(request, solicitud_id, respuesta):
    solicitud = SolicitudServicio.objects.get(id=solicitud_id)
    if respuesta == 'aceptar':
        # Si el médico acepta la solicitud, cambia el estado y crea el historial
        solicitud.estado = 'aceptado'
        solicitud.save()
        Historial.objects.create(
            user=solicitud.usuario_solicitante,
            subservicio=solicitud.subservicio,
            medico=solicitud.medico,
            direccion=solicitud.direccion
        )
    elif respuesta == 'rechazar':
        # Si rechaza, intenta reasignarlo a otro médico
        solicitud.estado = 'rechazado'
        solicitud.save()
        otro_medico = Medico.objects.filter(subservicios=solicitud.subservicio).exclude(id=solicitud.medico.id).first()
        if otro_medico:
            # Reasignar a otro médico
            solicitud.medico = otro_medico
            solicitud.estado = 'pendiente'
            solicitud.save()
        else:
            # Si no hay otro médico, deja la solicitud como pendiente sin médico asignado
            solicitud.medico = None
            solicitud.estado = 'pendiente'
            solicitud.save()
    return redirect('ver_solicitudes')

@login_required
def perfil_view(request):
    return render(request, 'servicios/perfil.html')
@login_required
def historial_servicios(request):
    historial = Historial.objects.filter(user=request.user)
    return render(request, 'historial.html', {'historial': historial})

@login_required
def perfil_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    servicios = Historial.objects.filter(medico=medico)
    return render(request, 'perfil_medico.html', {'medico': medico, 'servicios': servicios})

def seleccionar_servicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios})

def seleccionar_subservicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    subservicios = servicio.subservicios.all()
    return render(request, 'subservicios.html', {'servicio': servicio, 'subservicios': subservicios})


from geopy.distance import geodesic

from .models import Direccion, Medico, SubServicio, Historial
from django.shortcuts import get_object_or_404, redirect, render
from geopy.distance import geodesic


def asignar_direccion(request, subservicio_id):
    subservicio = get_object_or_404(SubServicio, id=subservicio_id)

    if request.method == 'POST':
        # Crear la dirección y obtener las coordenadas
        direccion = Direccion.objects.create(
            direccion=request.POST['direccion'],
            ciudad=request.POST['ciudad'],
            estado=request.POST['estado'],
            codigo_postal=request.POST['codigo_postal'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude']
        )

        # Verificar si se obtuvo correctamente la ubicación del usuario
        if direccion.latitude is None or direccion.longitude is None:
            return render(request, 'direccion.html', {
                'subservicio': subservicio,
                'error': "No se pudo obtener la ubicación del usuario."
            })

        # Filtrar médicos que ofrezcan el subservicio
        medicos = Medico.objects.filter(subservicios=subservicio)

        # Si no hay médicos disponibles para el subservicio
        if not medicos.exists():
            return render(request, 'direccion.html', {
                'subservicio': subservicio,
                'error': "No hay médicos disponibles para este servicio."
            })

        # Establecer el radio de búsqueda
        user_location = (float(direccion.latitude), float(direccion.longitude))
        medico_cercano = None
        distancia_minima = 10  # Radio en kilómetros

        for medico in medicos:
            # Verificar que el médico tiene coordenadas válidas
            if medico.latitude is None or medico.longitude is None:
                continue  # Saltar médicos sin ubicación válida

            # Calcular la distancia al médico
            medico_location = (float(medico.latitude), float(medico.longitude))
            distancia = geodesic(user_location, medico_location).kilometers

            # Seleccionar el médico más cercano dentro del radio
            if distancia <= distancia_minima:
                distancia_minima = distancia
                medico_cercano = medico

        # Si no se encontró ningún médico dentro del rango especificado
        if not medico_cercano:
            return render(request, 'direccion.html', {
                'subservicio': subservicio,
                'error': "No hay médicos disponibles cercanos en un radio de 10 km."
            })

        # Crear una solicitud de servicio con el médico más cercano asignado
        solicitud = SolicitudServicio.objects.create(
            subservicio=subservicio,
            direccion=direccion,
            usuario_solicitante=request.user,
            medico=medico_cercano,
            estado='pendiente'
        )

        # Redirige a la página de historial para ver la solicitud creada
        return redirect('historial_servicios')

    return render(request, 'direccion.html', {'subservicio': subservicio})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('servicios')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})
