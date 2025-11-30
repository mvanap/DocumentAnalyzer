
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('accounts/login/', views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    
    path('accounts/logout/', views.logout_view, name='logout'), 
    
    path('accounts/register/', views.register, name='register'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='chat/password_reset.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='chat/password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='chat/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='chat/password_reset_complete.html'), name='password_reset_complete'),
    
    path('settings/', views.settings_view, name='settings'),
    
    path('chat/', views.chat_view, name = 'chat'),
    
    path('accounts/profile/', views.profile, name='profile'),
    
    path('upload/', views.upload_patient_document, name='upload_patient_document'),
    
    path('patient/<str:patient_id>/files/', views.list_patient_files, name='patient_files'),
        
    path('', views.chat_view, name='chat_view'),
    
    path('get-response/', views.get_response, name='get_response'),
    
    
]

