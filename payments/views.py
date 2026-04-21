from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from buspass.models import StudentBusPass, RegularBusPass ,RenewalRequest

@login_required
def student_payment(request, token):
    app = get_object_or_404(StudentBusPass, payment_token=token)
    amount = 300

    if request.method == "POST":
        if  app.status == 'Approved':
            
            app.expiry_date = now().date() + timedelta(days=30)

            try:
                send_mail(
                "Student Bus Pass Payment Successful",
                f"Dear {app.name},\n\n"
                "Your E-Pass Details.\n\n"
                f"E-Pass ID : {app.epass_id}\n\n"
                f"Valid Till : {app.expiry_date}\n\n"
                "Thank you for using Online Bus Pass System.",
                settings.EMAIL_HOST_USER,
                [app.user.email],)

                app.status = 'Completed'            
                app.save()
                messages.success(request, "Payment successfully completed. Please check your email for E-Pass details.")

            except Exception:
                messages.error(request, "Payment Failed, Check your internet.")
                return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Student'})
            
        else:
            return HttpResponse('<h1>Payment already successfully completed. Please check your email for E-Pass details.<h1>')
        
        return redirect('student_epass', token=token)

    return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Student'})



@login_required
def regular_payment(request, token):
    app = get_object_or_404(RegularBusPass, payment_token=token)
    amount = 1000
    
    if request.method == "POST":
        if  app.status == 'Approved':
            
            app.expiry_date = now().date() + timedelta(days=30)

            try:
                send_mail(
                "Student Bus Pass Payment Successful",
                f"Dear {app.name},\n\n"
                "Your E-Pass Details.\n\n"
                f"E-Pass ID : {app.epass_id}\n\n"
                f"Valid Till : {app.expiry_date}\n\n"
                "Thank you for using Online Bus Pass System.",
                settings.EMAIL_HOST_USER,
                [app.user.email],)

                app.status = 'Completed'            
                app.save()
                messages.success(request, "Payment successfully completed. Please check your email for E-Pass details.")


            except Exception:
                messages.error(request, "Payment Failed, Check your internet.")
                return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Regular'})
            
        else:
            return HttpResponse('<h1>Payment already successfully completed. Please check your email for E-Pass details.<h1>')
        
        return redirect('regular_epass', token=token)

    return render(request, 'payments/payment.html', {'app': app,'amount': amount,'pass_type': 'Regular'})


@login_required
def student_renewal_payment(request, renewal_id):
    renewal = get_object_or_404(RenewalRequest,payment_token2=renewal_id,pass_type='Student')

    app = renewal.student_pass
    amount = 300

    if request.method == "POST":
        if renewal.status == 'Approved':
            # extend expiry
            app.expiry_date = now().date() + timedelta(days=30)

            try:
                send_mail(
                "Student Renewal Bus Pass Payment Successful",
                f"Dear {renewal.student_pass.name},\n\n"
                "Your E-Pass Details.\n\n"
                f"E-Pass ID : {app.epass_id}\n\n"
                f"Valid Till : {app.expiry_date}\n\n"
                "Thank you for using Online Bus Pass System.",
                settings.EMAIL_HOST_USER,
                [renewal.student_pass.user.email],)

                app.save()
                # update renewal
                renewal.status = 'Completed'
                renewal.save()

                messages.success(request, "Payment successfully completed. Please check your email for E-Pass details.")
                return redirect('student_epass', token=app.payment_token)
                
            except Exception:
                messages.error(request, "Payment Failed, Check your internet.")
                return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Student Renewal'})
           
        else:
            return HttpResponse('<h1>Payment already successfully completed. Please check your email for E-Pass details.<h1>')



    return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Student Renewal'})

@login_required
def regular_renewal_payment(request, renewal_id):
    renewal = get_object_or_404(RenewalRequest, payment_token2=renewal_id, pass_type='Regular')

    app = renewal.regular_pass
    amount = 1000

    if request.method == "POST":
        if renewal.status == 'Approved':
            # extend expiry
            app.expiry_date = now().date() + timedelta(days=30)

            try:
                send_mail(
                "Regular Bus Pass Payment Successful",
                f"Dear {renewal.regular_pass.name},\n\n"
                "Your E-Pass Details.\n\n"
                f"E-Pass ID : {app.epass_id}\n\n"
                f"Valid Till : {app.expiry_date}\n\n"
                "Thank you for using Online Bus Pass System.",
                settings.EMAIL_HOST_USER,
                [renewal.regular_pass.user.email],)

                app.save()
                # update renewal
                renewal.status = 'Completed'
                renewal.save()

                messages.success(request, "Payment successfully completed. Please check your email for E-Pass details.")
                return redirect('regular_epass', token=app.payment_token)
                
            except Exception:
                messages.error(request, "Payment Failed, Check your internet.")
                return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Regular Renewal'})
           
        else:
            return HttpResponse('<h1>Payment already successfully completed. Please check your email for E-Pass details.<h1>')

    return render(request, 'payments/payment.html', {'app': app, 'amount': amount, 'pass_type': 'Regular Renewal'})
