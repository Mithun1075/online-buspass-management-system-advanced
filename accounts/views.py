from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP
from django.contrib.auth.models import User

def generate_otp():
    return str(random.randint(1000, 9999))

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            otp = generate_otp()

            try:
                send_mail(
                    subject="OTP Verification - Online Bus Pass System",
                    message=(
                        f"Your OTP is {otp}. Do not share it.\n\n"
                        "Online Bus Pass System\n\n"
                        "Thank you"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                # -----

                check_email = EmailOTP.objects.filter(email=email).exists()
                
                if check_email:
                    up_otp = EmailOTP.objects.filter(email=email).first()
                    up_otp.otp=otp
                    up_otp.save() 

                else:
                # -----
                    EmailOTP.objects.create(email=email, otp=otp)
                    
                request.session['register_data'] = form.cleaned_data
                return redirect('verify_otp')

            except Exception:
                messages.error(request,"OTP could not be sent, Check your internet. Please try again.")
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        register_data = request.session.get('register_data')

        if not register_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        email = register_data.get('email')

        otp_obj = EmailOTP.objects.filter(email=email, otp=entered_otp).first()

        if otp_obj:
            if not User.objects.filter(username=register_data['username']).exists():
                User.objects.create_user(
                    username=register_data['username'],
                    email=email,
                    password=register_data['password1']
                )

            otp_obj.delete()
            del request.session['register_data']

            messages.success(request, "Registration successful.")
            return redirect('login')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'accounts/verify_otp.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            elif user.groups.filter(name='VerificationOfficer').exists():
                return redirect('officer_dashboard')

            else:
                return redirect('user_home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
