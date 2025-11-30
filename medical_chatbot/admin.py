from django.contrib import admin
from .models import PatientDocument

@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'patient_id', 'uploaded_at', 'size')
    search_fields = ('patient_id', 'file_name', 'uploaded_by_username')
    readonly_fields = ('uploaded_at',)