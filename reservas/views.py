from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Sala, Reserva, HorarioDisponivel

# Exibe uma lista de todas as salas cadastradas
def listar_salas(request):
    # Tive que considerar todas as salas, independentemente do status, para ser mais flexível
    salas = Sala.objects.all()
    return render(request, 'reservas/listar_salas.html', {'salas': salas})

# Função para validar e normalizar horários no formato 12 horas (AM/PM)
def validar_horario(hour_str):
    try:
        # Limpa espaços extras e formatações inconsistentes (AM/PM no padrão americano)
        hour_str = hour_str.strip().lower()
        hour_str = hour_str.replace('a.m.', 'am').replace('p.m.', 'pm')

        # Adiciona ":00" se os minutos não foram informados, já que isso é comum no uso diário
        if len(hour_str.split(":")) == 1:
            hour_str += ":00"

        # Verifica se o horário segue o padrão 12 horas
        datetime.strptime(hour_str, '%I:%M %p')  # Não converti para 24 horas por simplicidade
        return hour_str
    except ValueError:
        raise ValueError(f"Formato de hora inválido: {hour_str}")

# Formulário para realizar agendamentos de salas
def agendar_sala(request, sala_id):
    # Obtém a sala específica que o usuário quer agendar
    sala = get_object_or_404(Sala, id=sala_id)
    horarios_disponiveis = HorarioDisponivel.objects.filter(sala=sala)

    if request.method == 'POST':
        # Recebe os dados enviados pelo formulário
        data_agendamento = request.POST.get('data_agendamento')
        horario_inicio = request.POST.get('horario_inicio')
        horario_fim = request.POST.get('horario_fim')

        try:
            # Valida os horários (mantendo o formato 12 horas)
            horario_inicio_validado = validar_horario(horario_inicio)
            horario_fim_validado = validar_horario(horario_fim)
        except ValueError as e:
            # Retorna um erro caso o formato seja inválido
            return HttpResponse(f"Erro no formato da hora: {e}", status=400)

        # Combina a data com os horários validados
        horario_inicio_comb = f"{data_agendamento} {horario_inicio_validado}"
        horario_fim_comb = f"{data_agendamento} {horario_fim_validado}"

        try:
            # Converte as strings completas para objetos datetime
            horario_inicio_obj = datetime.strptime(horario_inicio_comb, '%Y-%m-%d %I:%M %p')
            horario_fim_obj = datetime.strptime(horario_fim_comb, '%Y-%m-%d %I:%M %p')

            # Verifica se o horário de início é anterior ao horário de término
            if horario_inicio_obj >= horario_fim_obj:
                return HttpResponse("Horário de início deve ser anterior ao horário de fim.", status=400)

            # Cria uma nova reserva
            reserva = Reserva.objects.create(
                sala=sala,
                usuario=request.user,
                horario_inicio=horario_inicio_obj,
                horario_fim=horario_fim_obj,
                status_reserva='C'  # Confirmada por padrão
            )

            # Atualiza o status da sala para "Indisponível"
            sala.status = 'I'
            sala.save()

            # Redireciona para a página de detalhes da reserva
            return redirect('detalhes_reserva', reserva_id=reserva.id)

        except ValueError as e:
            # Lida com erros no formato de data ou horário
            return HttpResponse(f"Erro no formato da data ou hora: {e}", status=400)

    return render(request, 'reservas/agendar_sala.html', {
        'sala': sala,
        'horarios_disponiveis': horarios_disponiveis
    })

# Exibe os detalhes de uma reserva específica
def detalhes_reserva(request, reserva_id):
    # Busca a reserva pelos seus detalhes
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'reservas/detalhes_reserva.html', {'reserva': reserva})
