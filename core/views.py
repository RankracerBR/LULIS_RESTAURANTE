from django.shortcuts import render

# Create your views here.

def pagina_principal(request):
    return render(request, 'index.html')

def pagina_mesas(request):
    ...

def pagina_admin(request):
    ...

def pagina_cadastro(request):
    ...