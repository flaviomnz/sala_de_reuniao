from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['horario_inicio', 'horario_fim']

    # garante que o horário de início seja antes do horário de fim...
    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')

        if horario_inicio >= horario_fim:
            raise forms.ValidationError('O horário de início deve ser anterior ao horário de fim.')
        return cleaned_data
