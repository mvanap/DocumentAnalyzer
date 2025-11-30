from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user_input = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_input[:50]}..."


# New model for uploaded patient documents
class PatientDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='patient_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document.name} uploaded by {self.user.username}"
