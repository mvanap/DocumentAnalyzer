from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication
    path('accounts/login/', LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'), 
    path('accounts/register/', views.register, name='register'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='chat/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='chat/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='chat/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='chat/password_reset_complete.html'), name='password_reset_complete'),

    # Settings & Profile
    path('settings/', views.settings_view, name='settings'),
    path('accounts/profile/', views.profile, name='profile'),

    # Chat
    path('chat/', views.chat_view, name='chat'),
    path('get-response/', views.get_response, name='get_response'),

    # Landing page
    path('', views.index_view, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
