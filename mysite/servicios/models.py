from django.db import models
from django.contrib.auth.models import User
from geopy.distance import geodesic  # Necesario para calcular distancias

class Direccion(models.Model):
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.direccion



class Servicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SubServicio(models.Model):
    servicio = models.ForeignKey(Servicio, related_name='subservicios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.servicio.nombre} - {self.nombre}"
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20)
    servicios = models.ManyToManyField(Servicio)
    subservicios = models.ManyToManyField(SubServicio)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def distance_to(self, lat, lon):
        return geodesic((self.latitude, self.longitude), (lat, lon)).kilometers
class SolicitudServicio(models.Model):
    subservicio = models.ForeignKey(SubServicio, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    usuario_solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud para {self.subservicio.nombre} - Estado: {self.estado}"

class Historial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subservicio = models.ForeignKey(SubServicio, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
