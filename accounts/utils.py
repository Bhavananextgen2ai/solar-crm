import random
from django.core.mail import send_mail
from .models import EmailOTP

def send_otp_email(user):
    otp = str(random.randint(100000, 999999))

    EmailOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject="Your Solar CRM Login OTP",
        message=f"Your OTP is {otp}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )
