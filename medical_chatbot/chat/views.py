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
import os
from django.conf import settings
    
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


@login_required
def chat_view(request):
    if request.method == 'POST':

        # 1️⃣ Get text question
        user_question = request.POST.get('question', '').strip()

        # 2️⃣ Check if file was uploaded
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            print("File received:", uploaded_file.name)
            print("Size:", uploaded_file.size)
            print("Content type:", uploaded_file.content_type)

            # Use absolute path based on MEDIA_ROOT
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)  # ensure folder exists

            save_path = os.path.join(upload_dir, uploaded_file.name)
            with open(save_path, "wb+") as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

            print("Saved file to:", save_path)

            return JsonResponse({
                'response': f"File '{uploaded_file.name}' uploaded successfully."
            })

        # 3️⃣ Handle normal text question
        if user_question:
            try:
                answer = Ask_AI(user_question, conversation_history)
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

