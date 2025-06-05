from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import UserProfile
from utils.email_utils import send_ses_email

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_ses_email(
                user.email,
                "Welcome to Our Platform!",
                f"Hi {user.email}, thanks for registering!"
            )
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = UserProfile.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                return redirect('profile')
            except UserProfile.DoesNotExist:
                error = 'Invalid credentials'
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = UserProfile.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})
