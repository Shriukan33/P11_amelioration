from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class AuthTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.connected_client = Client()
        self.connected_client.force_login(self.user)

    def test_login_page(self):
        url = reverse('authentification:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        url = reverse('authentification:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        url = reverse('authentification:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        url = reverse('authentification:profile', kwargs={
            'username': 'testuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_page_connected(self):
        url = reverse('authentification:profile', kwargs={
            'username': 'testuser'})
        response = self.connected_client.get(url)
        self.assertEqual(response.status_code, 200)
