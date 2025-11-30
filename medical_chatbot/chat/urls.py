
from django.urls import path
from . import views

urlpatterns = [
    
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    
    path('accounts/logout/', views.logout_view, name='logout'), 
    
    path('accounts/register/', views.register, name='register'),
    
    path('chat/', views.chat_view, name = 'chat'),
    
    path('accounts/profile/', views.profile, name='profile'),
    
    path('upload/', views.upload_patient_document, name='upload_patient_document'),
    
    path('patient/<str:patient_id>/files/', views.list_patient_files, name='patient_files'),
        
    path('', views.chat_view, name='chat_view'),
    
    path('get-response/', views.get_response, name='get_response'),
]
