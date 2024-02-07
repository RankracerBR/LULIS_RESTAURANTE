from django.db import models
from datetime import date

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=40, default='nome_completo')
    idade = models.IntegerField()
    email = models.EmailField()
    senha = models.TextField(max_length=150, verbose_name="Senha")
    imagem = models.ImageField(upload_to='imgs/')

class Reserva(models.Model):
    tickets = models.IntegerField(default=0)
    mesas = models.IntegerField()
    cadeiras = models.IntegerField()
    data = models.DateField(default=date.today)