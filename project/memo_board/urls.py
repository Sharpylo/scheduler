from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_views, name='base_views'),
    path('notes-list/', views.notes_list, name='notes_list'),
    path('note-create/', views.note_create, name='note_create'),
    path('note-edit/<int:item_id>/', views.note_edit, name='note_edit'),
    path('note-delete/<int:item_id>/', views.note_delete, name='note_delete'),
]
