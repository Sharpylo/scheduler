from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import RegisterForm


def sign_up(request: HttpRequest) -> HttpResponse:
    """
    Функция представления для регистрации нового пользователя.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        Объект ответа HTTP.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return HttpResponseRedirect('/')

    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})
