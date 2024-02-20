from django.test import TestCase, Client
from django.urls import reverse

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
        self.assertRedirects(response, reverse('pagina_principal'), fetch_redirect_response=False)

    def test_pagina_cadastro_POST_invalid_data(self):
        invalid_data = {'username': 'testuser'}
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200) 

    def test_pagina_cadastro_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200) 

class CadastroReservaTestCase(TestCase):
    ...

class LoginUsuarioTestCase(TestCase):
    ...