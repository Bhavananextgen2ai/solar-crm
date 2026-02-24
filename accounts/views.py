import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail


# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


# ---------------- EMAIL OTP LOGIN ----------------
from django.db.models import Q

def email_login(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            messages.error(request, "Email not registered")
            return redirect("login")

        otp = random.randint(100000, 999999)

        request.session['otp'] = otp
        request.session['email'] = user.email  # use DB email

        print("OTP:", otp)

        send_mail(
            "Your Solar CRM Login OTP",
            f"Your OTP is {otp}",
            "bbhavanadm@gmail.com",
            [user.email],
            fail_silently=False
        )

        return redirect("verify_otp")

    return render(request, "accounts/login.html")



# ---------------- VERIFY OTP ----------------
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        email = request.session.get("email")

        if str(entered_otp) == str(session_otp):
            user = User.objects.get(email__iexact=email)

            login(request, user)

            # Clear session
            request.session.pop('otp', None)
            request.session.pop('email', None)

            return redirect("home")  # change to home

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify_otp.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("login")
