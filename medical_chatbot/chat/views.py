from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ChatMessage
from .AI.response import Ask_AI, conversation_history  # Import from your file
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
    
# Root URL (/) - Landing page with login prompt
def index_view(request):
    
    if request.user.is_authenticated:
    
        return redirect('chat')  # If already logged in, go to chat
    
    return render(request, 'chat/index.html')  # Show login page for guests

def register(request):
    """
    Register a new user using Django's built-in UserCreationForm.
    On success, auto-login the user and redirect to LOGIN_REDIRECT_URL.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')  # redirect after successful registration
        else:
            messages.error(request, "Please fix the errors below.")
            # ✅ Render the form again with errors
            return render(request, 'chat/register.html', {'form': form})
    
    else:
        form = UserCreationForm()
        return render(request, 'chat/register.html', {'form': form})

    
def logout_view(request):
    """
    Simple Logout. keeps it explicit rather than relying on a class.
    """
    logout(request)
    messages.info(request, "Logged Out. ")
    return redirect('login')

def settings_view(request):
    return render(request, 'chat/settings.html')

@login_required

def profile(request):
    """
    Minimal Profile page to test that auth works
    """
    return render(request, 'chat/profile.html')


@login_required  # Add this if uploads should require login
def upload_patient_document(request):
    if request.method == 'POST':
        form = PatientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            uploaded_file = request.FILES['document']
            doc.file_name = uploaded_file.name
            doc.content_type = uploaded_file.content_type
            doc.size = uploaded_file.size
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "File uploaded successfully.")
            return redirect('patient_files', patient_id=doc.patient_id)
        # No else here - fall through to render
    else:
        form = PatientDocumentForm()  # For GET requests
    return render(request, 'chat/upload.html', {'form': form})
        
@login_required  # Add if needed
def list_patient_files(request, patient_id):
    qs = PatientDocument.objects.filter(patient_id=patient_id).order_by("-uploaded_at")
    if not request.user.is_staff:
        qs = qs.filter(uploaded_by=request.user)  # Non-staff only see their uploads
    return render(request, 'chat/upload.html', {
        'object_list': qs,
        'form': PatientDocumentForm(initial={'patient_id': patient_id})  # Fixed key
    })

@login_required
def chat_view(request):
    if request.method == 'POST':
        user_question = request.POST.get('question', '').strip()
        if user_question:
            try:
                # Call your existing Ask_AI function
                answer = Ask_AI(user_question, conversation_history)
                # Save to DB (optional)
                ChatMessage.objects.create(user_input=user_question, ai_response=answer)
                return JsonResponse({'response': answer})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'Empty question'}, status=400)
    return render(request, 'chat/chat.html')

@login_required
def get_response(request):
    user_message = request.GET.get('message', '').strip()
    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    try:
        answer = Ask_AI(user_message, conversation_history)
        return JsonResponse({'response': answer})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

