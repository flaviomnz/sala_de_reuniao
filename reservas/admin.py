from django.contrib import admin
from .models import Sala, Reserva, HorarioDisponivel

class HorarioDisponivelInline(admin.TabularInline):
    model = HorarioDisponivel
    extra = 1  # Número de linhas extras para adicionar novos horários

# Personalizando a administração para reservas
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'usuario', 'horario_inicio', 'horario_fim', 'status_reserva')  # Como as reservas vão aparecer na lista
    list_filter = ('status_reserva', 'sala', 'usuario')  # Facilita a busca e filtragem no admin

class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'capacidade', 'status', 'exibir_horarios_disponiveis']  
    search_fields = ['nome']  
    list_filter = ['status']  # Filtro para facilitar encontrar salas ativas ou inativas
    inlines = [HorarioDisponivelInline]  # Exibe horários disponíveis diretamente no formulário de sala


    def exibir_horarios_disponiveis(self, obj):
        # Cria uma string com todos os horários disponíveis para a sala
        return ", ".join([f"{horario.horario_inicio.strftime('%H:%M')} - {horario.horario_fim.strftime('%H:%M')}" for horario in obj.horarios_disponiveis.all()])
    exibir_horarios_disponiveis.short_description = 'Horários Disponíveis'  

    # Formulário de edição da sala no admin
    fieldsets = (
        (None, {
            'fields': ('nome', 'capacidade', 'recursos_disponiveis', 'status')  # Campos para edição de dados da sala
        }),
    )

# Parte que registra as salas, reservas e horários no painel de administração
admin.site.register(Sala, SalaAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(HorarioDisponivel)
