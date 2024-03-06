from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

# Create your models here.

class Usuario(AbstractUser):
    idade = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='imgs/', default="Imagens")
    
    def __str__(self):
        return self.username if self.username else str(self.pk)

    def __reduce__(self):
        # Retorna None para indicar que nenhum processo de redução é necessário
        return None

class RegistroToken(models.Model):
    nome = models.CharField(max_length=50, default='', blank=True)
    email = models.EmailField()

    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100, default='token')

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    preco_aluguel = models.IntegerField()
    limite_reserva = models.IntegerField(default=0)

    def __str__(self):
        return f'Mesa {self.numero}'

    def total_reservas(self):
        return self.reserva_set.count()

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tickets = models.IntegerField(default=0)
    mesa = models.ForeignKey(Mesa,on_delete=models.CASCADE)
    data = models.DateField(default=date.today)

    def __str__(self):
        return (f'Reserva de {self.usuario.username} '
                f' para Mesa {self.mesa.numero} em {self.data}')