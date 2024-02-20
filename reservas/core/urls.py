from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from core import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('enviar_token', views.registrar_token, name='registrar_token'),
    path('cadastro_usuario/', views.pagina_cadastro, name="pagina_cadastro"),
    path('login/', views.pagina_login, name="pagina_login"),
    path('verify/<str:token>', views.verificar, name='verificar'),
    #path('logout/'),
    path('mesas', views.pagina_mesas, name="pagina_mesas"),
    re_path(r'^\d+/$', views.pagina_principal, name='catch_all')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)