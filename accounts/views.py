from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # ✅ CREATE USER (IMPORTANT)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid password")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

from .models import EmailOTP

def otp_verify(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        user_id = request.session.get("otp_user")

        otp_obj = EmailOTP.objects.filter(
            user_id=user_id,
            otp=otp_input
        ).last()

        if otp_obj:
            login(request, otp_obj.user)
            EmailOTP.objects.filter(user=otp_obj.user).delete()
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "accounts/otp_verify.html")
