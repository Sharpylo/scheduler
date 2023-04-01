from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Note
from .forms import NoteForm


# Тест для модели

class NoteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        self.note = Note.objects.create(
            title='Test Note',
            text='This is a test note.',
            user=self.user)

    def test_can_edit(self):
        # Test that the owner of the note can edit it
        self.assertTrue(self.note.can_edit(self.user))

        # Test that a different user cannot edit the note
        other_user = User.objects.create_user(
            username='otheruser', password='password456')
        self.assertFalse(self.note.can_edit(other_user))

    def test_str(self):
        # Test that the string representation of the note is its title
        self.assertEqual(str(self.note), 'Test Note')


# Тесты для формы

class TestNoteForm(TestCase):
    def test_note_form_valid_data(self):
        form_data = {
            'title': 'Test Title',
            'text': 'Test Text'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_note_form_missing_data(self):
        form_data = {
            'title': '',
            'text': ''
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertTrue('title' in form.errors)
        self.assertTrue('text' in form.errors)


# Тесты для представлений

class NoteCreateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.note_data = {'title': 'Test Note', 'text': 'This is a test note.'}
        self.url = reverse('note_create')

    def test_note_create_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, self.note_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes_list'))
        note = Note.objects.first()
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.text, 'This is a test note.')
        self.assertEqual(note.user, self.user)

    def test_note_create_view_with_unauthenticated_user(self):
        response = self.client.post(self.url, self.note_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + self.url)
        self.assertEqual(Note.objects.count(), 0)


class NoteEditTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.note = Note.objects.create(title='Test Note', text='This is a test note.', user=self.user1)
        self.url = reverse('note_edit', args=[self.note.id])
        self.valid_data = {'title': 'Updated Test Note', 'text': 'This is an updated test note.'}
        self.invalid_data = {'title': '', 'text': ''}

    def test_note_edit_view_with_authenticated_user_and_valid_data(self):
        self.client.login(username='testuser1', password='testpass')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes_list'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Test Note')
        self.assertEqual(self.note.text, 'This is an updated test note.')

    def test_note_edit_view_with_authenticated_user_and_invalid_data(self):
        self.client.login(username='testuser1', password='testpass')
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_note_edit_view_with_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_note_edit_view_with_authenticated_user_but_not_note_owner(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('note_edit', kwargs={'item_id': self.note.id}))
        self.assertEqual(response.status_code, 403)

        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.text, 'This is a test note.')


class NoteDeleteTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.note = Note.objects.create(title='Test Note', text='This is a test note.', user=self.user1)
        self.url = reverse('note_delete', args=[self.note.id])

    def test_note_delete_view_with_authenticated_user_and_note_owner(self):
        self.client.login(username='testuser1', password='testpass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes_list'))
        self.assertFalse(Note.objects.filter(pk=self.note.id).exists())

    def test_note_delete_view_with_authenticated_user_but_not_note_owner(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Note.objects.filter(pk=self.note.id).exists())

    def test_note_delete_view_with_unauthenticated_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(pk=self.note.id).exists())

    def test_note_delete_view_with_nonexistent_note(self):
        nonexistent_url = reverse('note_delete', args=[self.note.id + 1])
        self.client.login(username='testuser1', password='testpass')
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.note = Note.objects.create(title='Test note', text='Test text', user=self.user)

    def test_can_edit(self):
        self.assertTrue(self.note.can_edit(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='anotherpass')
        self.assertFalse(self.note.can_edit(another_user))
