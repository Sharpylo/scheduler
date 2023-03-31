from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_per_page = 20


admin.site.register(Note, NoteAdmin)
