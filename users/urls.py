from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import activate, password_reset

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register_info/', views.TemplateView.as_view(template_name='users/register_info.html'), name='register_info'),
    path('register_done/', views.TemplateView.as_view(template_name='users/register_done.html'), name='register_done'),
    path('register_error/', views.TemplateView.as_view(template_name='users/register_error.html'), name='register_error'),
    path('password_reset/', password_reset, name='password_reset_form'),
    path('password_reset/done/', views.TemplateView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
]
