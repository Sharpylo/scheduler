from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    title: forms.CharField = forms.CharField(label='Наименование заметки')
    text: forms.CharField = forms.CharField(label='Заметка', widget=forms.Textarea)

    class Meta:
        model: Note = Note
        fields: list = ['title', 'text']
