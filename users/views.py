import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users import forms
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

from django.contrib.auth.views import FormView
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

from users.token import account_activation_token





class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_info')

    def form_valid(self, form):
        # Сохранение пользователя
        user = form.save(commit=False)
        user.is_active = False
        user.save()



        # Получение текущего сайта
        current_site = get_current_site(self.request)

        # Подготовка данных для отправки электронного письма

        mail_subject = 'Теперь вы зарегистрированы на нашем сервисе! Подтвердите свой электронный адрес.'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return super().form_valid(form)

    def form_invalid(self, form):
        form = UserRegisterForm
        return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()

        group = Group.objects.get(name='Право на изменение')
        user.groups.add(group)
        return redirect(reverse('users:register_done'))
    else:
        return redirect(reverse('users:register_error'))





def password_reset(request):

    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'users/password_reset_form.html', {'error_message': 'Пользователь с таким email не найден'})
        new_password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
        send_mail(
            subject='Вы сменили пароль',
            message=f'ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        user.set_password(new_password)
        user.save()

        return redirect(reverse('users:password_reset_done'))
    return render(request, 'users/password_reset_form.html')


