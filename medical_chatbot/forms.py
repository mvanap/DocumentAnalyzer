

def patient_document_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.patient_id}_{uuid.uuid4().hex}.{ext}"
    return os.path.join('patient_documents', filename)

class PatientDocument(models.Model):
    patient_id = models.CharField(max_length=100, db_index=True)
    uploaded_by=
    
    