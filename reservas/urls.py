from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_salas, name='listar_salas'),
    path('agendar/<int:sala_id>/', views.agendar_sala, name='agendar_sala'),
    path('detalhes_reserva/<int:reserva_id>/', views.detalhes_reserva, name='detalhes_reserva'),
]
