from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Reserva, Mesa
from django.contrib import admin
from .forms import UsuarioRegistroForm

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioRegistroForm
    list_display = ('username', 'email', 'imagem')
    list_filter =  ('username', 'email', 'imagem')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'description', 'imagem')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('tickets','mesa','data')
    list_filter = ('tickets','mesa','data',)

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'preco_aluguel')
    list_filter = ('numero','preco_aluguel',)