from django.conf.urls.static import static
from django.urls import path, re_path
from django.conf import settings
from core import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('enviar_token', views.registrar_token, name='registrar_token'),
    path('cadastro_usuario/', views.pagina_cadastro, name="pagina_cadastro"),
    path('login/', views.pagina_login, name="pagina_login"),
    path('verify/<str:token>', views.verificar, name='verificar'),
    path('pagina_usuario/', views.pagina_usuario, name="pagina_usuario"),
    path('pagina_usuario/mesas', views.pagina_mesas,
          name="pagina_usuario_mesas"),
    path('pagina_usuario/mesas/mesastotais', views.pagina_reservas_totais, 
         name="pagina_usuario_mesas_reservas_totais"),
    path('logout', views.funcao_logout, name="logout"),
    path('pagamento/', views.pagina_pagamento, name="pagamento")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)