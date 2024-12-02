from django.db import models
from django.contrib.auth.models import User

class Sala(models.Model):
    nome = models.CharField(max_length=255)
    capacidade = models.IntegerField()
    recursos_disponiveis = models.TextField()
    status = models.CharField(max_length=1, choices=[('A', 'Ativa'), ('I', 'Inativa')])

    def __str__(self):
        return self.nome

class HorarioDisponivel(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="horarios_disponiveis")
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def __str__(self):
        return f"{self.sala.nome} - {self.horario_inicio} a {self.horario_fim}"

class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    horario_inicio = models.DateTimeField()
    horario_fim = models.DateTimeField()
    status_reserva = models.CharField(max_length=1, choices=[('C', 'Confirmada'), ('P', 'Pendente')], default='P')

    def __str__(self):
        return f"Reserva de {self.sala.nome} por {self.usuario.username}"
