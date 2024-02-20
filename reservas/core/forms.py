from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, RegistroToken, Reserva
from django import forms

class UsuarioRegistroForm(UserCreationForm):
    idade = forms.IntegerField(initial=0)

    class Meta:
        model = Usuario
        fields = ['username', 'idade', 'email', 'imagem']

class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroToken
        fields = ('nome','email')
        labels = {
            'nome': 'Nome'
        }

class ReservasForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['mesa', 'tickets']