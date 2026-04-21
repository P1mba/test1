from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser
# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("users:profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "main/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form  = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("users:profile")
    else:
        form = CustomUserLoginForm()
    return render(request, "main/login.html", {'form': form})

@login_required
def profile_view(request):
    return render(request, 'main/profile.html', {"user": request.user})

@login_required
def account_detail(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'main/partials/account_details.html',
                  {"user": user})

@login_required
def edit_account_details(request):
    form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'main/partials/edit_account_details.html',
                  {"user": request.user, "form": form})

@login_required
def update_account_details(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
            return render(request, 'main/partials/account_details.html', {"user": user})
        else:
            return render(request, 'main/partials/account_details.html', {"user": request.user, "form": form})
    return render(request, 'main/partials/account_details.html', {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect('users:register')

