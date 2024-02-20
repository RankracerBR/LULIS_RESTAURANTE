from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioRegistroForm, RegistroForm, ReservasForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from core.models import RegistroToken, Mesa
from datetime import date
import random

# Create your views here.

def pagina_principal(request):
    return render(request, 'index.html')

def pagina_cadastro(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request,usuario)
            return redirect('pagina_principal')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'cadastro.html', {'form': form})

def pagina_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pagina_mesas')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def pagina_mesas(request):
    if request.method == 'POST':
        form = ReservasForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.data = date.today()

            mesa_escolhida = form.cleaned_data['mesa']

            reserva.valor = mesa_escolhida.preco_aluguel * reserva.tickets

            reserva.save()
            return redirect('pagina_principal')

    else:
        form = ReservasForm()

    mesas_disponiveis = Mesa.objects.all()
    
    return render(request, 'reservas.html', {'form': form, 'mesas_disponiveis': mesas_disponiveis})

def registrar_token(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.token = str(random.random()).split('.')[1]
            user.save()

            domain_name = get_current_site(request).domain
            link = f'http://{domain_name}/verify/{user.token}'        
            send_mail(
                'Verificação de Email',
                f'Clique para completar seu cadastro: {link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return HttpResponse('Verifique a caixa de entrada do seu email para confirmar')
    else:
        form = RegistroForm()
    return render(request, 'enviar_token.html', {'form': form})

def verificar(request, token):
    try:
        user = RegistroToken.objects.get(token=token)
        user.is_verified = True
        user.save()
        return redirect('pagina_cadastro')
    except RegistroToken.DoesNotExist:
        return render(request, 'cadastro.html')


