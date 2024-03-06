from core.models import Usuario, Reserva, RegistroToken
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from .models import Mesa


# Create your tests here.

class TestPaginaCadastro(TestCase):
    def setUp(self):
        self.url = reverse('pagina_cadastro')
        self.data = {
            'username': 'testuser',
            'idade': 25,
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_pagina_cadastro_POST_valid_data(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina_principal'), 
                             fetch_redirect_response=False)

    def test_pagina_cadastro_POST_invalid_data(self):
        invalid_data = {'username': 'testuser'}
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200) 

    def test_pagina_cadastro_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200) 

class LoginUsuarioTestCase(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(username='testuser',
                                                 password='12345')

    def test_pagina_login_GET(self):
        response = self.client.get(reverse('pagina_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_pagina_login_POST_valid_credentials(self):
        form_data = {
            'username': 'testuser',
            'password': '12345'
        }
        response = self.client.post(reverse('pagina_login'), form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina_usuario'))

    def test_pagina_login_POST_invalid_credentials(self):
        form_data = {
            'username': 'testuserr',
            'password': '123453'
        }
        response = self.client.post(reverse('pagina_login'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        message_to_find = ('Por favor, entre com um usuário e senha corretos.'
                          ' Note que ambos os campos diferenciam maiúsculas e'
                          ' minúsculas.')
        response_content = response.content.decode()
        self.assertFalse(f'<li>{message_to_find.strip().lower()}</li>' in 
                         response_content.strip().lower())

class CadastroReservaTestCase(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(username='testuser', 
                                                password='12345')

        self.mesa1 = Mesa.objects.create(numero=1, preco_aluguel=50, 
                                         limite_reserva=3)
    
    def test_pagina_mesas_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pagina_usuario_mesas')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas.html')

    def test_pagina_mesas_POST(self):
        self.client.force_login(self.user)
        form_data = {
            'usuario': self.user.id,
            'tickets': 2,
            'mesa': self.mesa1.id,
            'data': '2024-02-23'
        }
        response = self.client.post(reverse('pagina_usuario_mesas'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina_usuario'))

        self.assertEqual(Reserva.objects.count(), 1)
        reserva = Reserva.objects.first()
        self.assertEqual(reserva.usuario, self.user)
        self.assertEqual(reserva.tickets, 2)
        self.assertEqual(reserva.mesa, self.mesa1)
    
    def test_pagina_mesas_post_no_tickets(self):
        self.client.force_login(self.user)
        form_data = {
            'usuario': self.user.id,
            'tickets': 0,  # ou remova completamente o campo 'tickets' do formulário
            'mesa': self.mesa1.id,
            'data': '2024-02-23'
        }
        response = self.client.post(reverse('pagina_usuario_mesas'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina_usuario_mesas'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nenhum ticket foi digitado')

        self.assertEqual(Reserva.objects.count(), 0)

    def test_pagina_mesas_POST_limite_reserva_atingido(self):
        self.client.force_login(self.user)
        
        # Faça reservas até atingir o limite
        for _ in range(self.mesa1.limite_reserva):
            form_data = {
                'usuario': self.user.id,
                'tickets': 1,
                'mesa': self.mesa1.id,
                'data': '2024-02-23'
            }
            response = self.client.post(reverse('pagina_usuario_mesas'), form_data)
            self.assertEqual(response.status_code, 302)
        
        # Agora, tente fazer uma reserva além do limite
        form_data_limite_atingido = {
            'usuario': self.user.id,
            'tickets': 1,
            'mesa': self.mesa1.id,
            'data': '2024-02-23'
        }
        response_limite_atingido = self.client.post(reverse('pagina_usuario_mesas'), form_data_limite_atingido)
        
        messages = list(get_messages(response_limite_atingido.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Limite de reservas atingido')
    
        self.assertEqual(Reserva.objects.count(), self.mesa1.limite_reserva)


class TokenRegistroTestCase(TestCase):
    def test_registrar_token(self):
        user_data = {'username': 'testuser', 'email': 'test@example.com', 
                     'password': 'testpass'}
        response = self.client.post(reverse('registrar_token'), data=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(RegistroToken.objects.count(), 1)
        self.assertFalse(RegistroToken.objects.first().is_verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Verificação de Email', mail.outbox[0].subject)
    
    def test_verificar_token(self):
        token = RegistroToken.objects.create(token='testtoken')
        response = self.client.get(reverse('verificar', args=[token.token]))
    
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina_cadastro'))