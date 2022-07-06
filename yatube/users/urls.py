from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_change/', PasswordChangeView.as_view(), name='password_change_form'
    ),
    path(
        'password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'
    ),
    path(
        'password_reset', PasswordResetView.as_view(), name='password_reset_form'
    ),
    path(
        'password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'
    ),
    path(
        'reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'
    ),
]
