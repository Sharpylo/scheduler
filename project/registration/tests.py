from django.contrib.auth.forms import UserCreationForm
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .forms import RegisterForm


# тест для формы
class RegisterFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'weak',
            'password2': 'weaker',
        }

    def test_register_form_with_valid_data(self):
        form = UserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(username='testuser').exists())


# тест для представления
class SignUpViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('sign_up')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'weak',
            'password2': 'weaker',
        }

    def test_sign_up_with_valid_data(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_sign_up_with_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='').exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_sign_up_with_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html')
        self.assertTrue(isinstance(response.context['form'], RegisterForm))
