from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404

from .models import Note
from .forms import NoteForm


@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return HttpResponseRedirect(reverse('notes_list'))
    else:
        form = NoteForm()
    return render(request, 'memo_board/note_create.html', {'form': form})


@login_required
def note_edit(request, item_id):
    note = get_object_or_404(Note, id=item_id)
    if not note.can_edit(request.user):
        return HttpResponseForbidden('Вы не авторизованы для выполнения этого действия')
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('notes_list'))
    return render(request, 'memo_board/note_edit.html', {'form': form})


@login_required
def note_delete(request, item_id):
    try:
        note = Note.objects.get(pk=item_id)
        if not note.can_edit(request.user):
            return HttpResponseForbidden('Вы не уполномочены выполнять это действие')
        note.delete()
        return HttpResponseRedirect(reverse('notes_list'))
    except Note.DoesNotExist:
        return HttpResponse('Заметка не существует', status=404)


@login_required
def notes_list(request):
    notes_list = Note.objects.all().order_by('-user')
    context = {'notes_list': notes_list}
    return render(request, 'memo_board/notes_list.html', context=context)


def base_views(request):
    return render(request, 'memo_board/base.html')
