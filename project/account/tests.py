from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile


# тест для модели
class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_profile_creation(self):
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.phone_number = '1234567890'
        profile.bio = 'Hello, I am a test user!'
        profile.save()
        self.assertFalse(created)


# Тест для форм
class UserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_valid_form(self):
        form = UserUpdateForm(data={'username': 'newusername', 'email': 'newemail@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserUpdateForm(data={'username': '', 'email': ''}, instance=self.user)
        self.assertFalse(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        try:
            self.profile = Profile.objects.get(user=self.user)
        except Profile.DoesNotExist:
            self.profile = Profile.objects.create(user=self.user, phone_number='1234567890', bio='')

    def test_valid_form(self):
        data = {'phone_number': '0987654321', 'bio': 'Test Bio'}
        form = ProfileUpdateForm(data=data, instance=self.profile)
        self.assertTrue(form.is_valid(), msg=form.errors.as_text())  # выводим ошибки валидации формы
        form.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, '0987654321')
        self.assertEqual(self.profile.bio, 'Test Bio')

    def test_invalid_form(self):
        data = {'phone_number': ''}
        form = ProfileUpdateForm(data=data, instance=self.profile)
        self.assertFalse(form.is_valid())


# тест для представлений
class AccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_account_view_with_valid_data(self):
        url = reverse('account')
        response = self.client.post(url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'bio': 'Hello, I am a test user!',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected to account page
        self.assertEqual(response.url, reverse('account'))
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.bio, 'Hello, I am a test user!')

    def test_account_view_with_invalid_data(self):
        url = reverse('account')
        response = self.client.post(url, {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'phone_number': '1234567890',
            'bio': 'Hello, I am a test user!',
        })
        self.assertEqual(response.status_code, 200)  # Check if form errors are shown
        self.assertContains(response, 'This field is required.')  # Check for error message
        self.assertTemplateUsed(response, 'account/account.html')  # Check if the correct template is used
