from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display: tuple = ('title', 'user')
    list_per_page: int = 20


admin.site.register(Note, NoteAdmin)
