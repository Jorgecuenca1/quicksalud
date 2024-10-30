from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('servicios/', views.seleccionar_servicio, name='servicios'),
    path('servicios/<int:servicio_id>/', views.seleccionar_subservicio, name='seleccionar_subservicio'),
    path('direccion/<int:subservicio_id>/', views.asignar_direccion, name='asignar_direccion'),
    path('historial/', views.historial_servicios, name='historial_servicios'),
    path('solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
    path('solicitudes/<int:solicitud_id>/<str:respuesta>/', views.responder_solicitud, name='responder_solicitud'),

]
