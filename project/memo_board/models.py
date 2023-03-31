from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование заметки')
    text = models.TextField(max_length=250, verbose_name='Заметка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def can_edit(self, user):
        return user == self.user

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
