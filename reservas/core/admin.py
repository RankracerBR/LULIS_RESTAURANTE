from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Reserva, Mesa
from django.contrib import admin
from .forms import UsuarioRegistroForm
from django.conf import settings
from django.contrib import messages
import psycopg2
import boto3

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioRegistroForm
    list_display = ('username', 'email', 'imagem')
    list_filter =  ('username', 'email', 'imagem')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 
                                             'imagem')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                   'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    def exportar_para_dynamodb(self, request, queryset):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        aws_default_region = settings.AWS_DEFAULT_REGION

        dynamodb = boto3.resource('dynamodb',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=aws_default_region)

        table = dynamodb.Table('UsuariosGutosRestaurante')

        for user in queryset:
            table.put_item(
                Item={
                    'Partition2': user.username,
                    'email': user.email,
                    'idade': user.idade,
                    'imagem': str(user.imagem), 
                }
            )
        self.message_user(request, 
                          "Os dados foram enviados para o DynamoDB com sucesso")

    exportar_para_dynamodb.short_description = "Exportar para o DynamoDB"
    actions = [exportar_para_dynamodb]

# Em testes
    def exportar_para_RDS(self, request, queryset):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        aws_default_region = settings.AWS_DEFAULT_REGION

        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )

        cursor = conn.cursor()

        for user in queryset:
            cursor.execute( ##EDITAR
                "INSERT INTO ",
                (user.username, user.email, user.idade)
            )
        
        conn.commit()
        conn.close()

        self.message_user(request, 
                          "Os dados foram enviados para o RDS com sucesso")

    exportar_para_RDS.short_description = "Exportar para o RDS"
    actions = [exportar_para_RDS]

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('tickets','mesa','data')
    list_filter = ('tickets','mesa','data',)

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'preco_aluguel','limite_reserva')
    list_filter = ('numero','preco_aluguel','limite_reserva')