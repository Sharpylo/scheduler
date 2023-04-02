from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from django.conf import settings
import os

from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender: User, instance: User, created: bool, **kwargs) -> None:
    """
    Функция приемника сигналов для создания профиля и установки стандартного изображения профиля
    для вновь созданного пользователя.

    Args:
        sender: Класс модели отправителя.
        instance: Фактический сохраняемый экземпляр.
        created: A boolean; Истина, если была создана новая запись.

    Returns:
        None
    """
    if created:
        default_img_path = os.path.join(settings.BASE_DIR, 'media', 'account.jpg')
        with open(default_img_path, 'rb') as f:
            file = File(f)
            profile = Profile.objects.create(user=instance)
            profile.image.save('account.jpg', file)


@login_required
def account(request) -> render:
    """
    Функция просмотра для отображения страницы счета.

    Args:
        request: HTTP-запрос.

    Returns:
        HTTP-ответ, содержащий отрисованный шаблон.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/account.html', context)


def profile(request, username: str) -> render:
    """
    Функция представления для вывода страницы профиля пользователя.

    Args:
        request: HTTP-запрос..
        username: Имя пользователя, профиль которого отображается.

    Returns:
        HTTP-ответ, содержащий отрисованный шаблон.
    """
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'account/profile.html', context)
