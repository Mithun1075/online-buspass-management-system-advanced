from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from buspass.models import StudentBusPass, RegularBusPass, RenewalRequest


# officer check

def is_officer(user):
    return user.groups.filter(name='VerificationOfficer').exists()
    
# dashboard

@user_passes_test(is_officer)
def officer_dashboard(request):
    return render(request, 'officer/officer_dashboard.html')

# new apply pending

@user_passes_test(is_officer)
def new_apply_pending_list(request):
    return render(
        request,
        'officer/new_apply_pending_list.html',
        {
            'student_pending': StudentBusPass.objects.filter(status='Pending'),
            'regular_pending': RegularBusPass.objects.filter(status='Pending'),
        }
    )

# renewal pending list

@user_passes_test(is_officer)
def renewal_pending_list(request):
    return render(request,'officer/renewal_pending_list.html',
        {
            'student_renewals': RenewalRequest.objects.filter(status='Pending', pass_type='Student'),
            'regular_renewals': RenewalRequest.objects.filter(status='Pending', pass_type='Regular'),
        }
    )

# approve new student 

@user_passes_test(is_officer)
def approve_student(request, pk):
    app = get_object_or_404(StudentBusPass, id=pk)

    payment_link = f"http://127.0.0.1:8000/payments/student/{app.payment_token}/"

    try:
        send_mail(
            subject="Bus Pass Approved – Payment Required",
            message=(
                f"Dear {app.name},\n\n"
                "Your STUDENT bus pass application has been approved.\n\n"
                f"Payment link:\n{payment_link}\n\n"
                "Thank you."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[app.user.email],
            fail_silently=False,
        )

        app.status = 'Approved'
        app.save()
        messages.success(request, "Approved & email sent")

    except Exception:
        messages.error(request,"Email could not be sent, Check your internet. Application remains pending.")

    return redirect('new_apply_pending_list')

# approve new regular

@user_passes_test(is_officer)
def approve_regular(request, pk):
    app = get_object_or_404(RegularBusPass, id=pk)

    payment_link = f"http://127.0.0.1:8000/payments/regular/{app.payment_token}/"

    try:
        send_mail(
            subject="Bus Pass Approved – Payment Required",
            message=(
                f"Dear {app.name},\n\n"
                "Your REGULAR bus pass application has been approved.\n\n"
                f"Payment link:\n{payment_link}\n\n"
                "Thank you."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[app.user.email],
            fail_silently=False,
        )

        app.status = 'Approved'
        app.save()

        messages.success(request, "Approved & email sent")

    except Exception:
        messages.error(request,"Email could not be sent, Check your internet. Application remains pending.")

    return redirect('new_apply_pending_list')



# approve reneval

@user_passes_test(is_officer)
def approve_renewal(request, pk):
    renewal = get_object_or_404(RenewalRequest, id=pk)

    if renewal.status != 'Pending':
        messages.warning(request, "This renewal request is already processed.")
        return redirect('renewal_pending_list')

    buspass = (renewal.student_pass if renewal.pass_type == 'Student'else renewal.regular_pass)

    payment_link = (
        f"http://127.0.0.1:8000/payments/renewal/"
        f"{renewal.pass_type.lower()}/{renewal.payment_token2}/"
    )

    try:
        send_mail(
            subject="Bus Pass Renewal Approved – Payment Required",
            message=(
                f"Dear {buspass.name},\n\n"
                "Your bus pass renewal request has been approved.\n"
                "Please complete payment to extend validity.\n\n"
                f"Payment link:\n{payment_link}\n\n"
                "Thank you."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[renewal.user.email],
            fail_silently=False,
        )

        renewal.status = 'Approved'
        renewal.save()

        messages.success(request, "Renewal approved & payment link sent")

    except Exception:
        messages.error(request,"Email could not be sent, Check your internet. Renewal remains pending.")

    return redirect('renewal_pending_list')


# reject and reason

@user_passes_test(is_officer)
def reject_with_reason(request, model, pk):

    if model == 'student':
        obj = get_object_or_404(StudentBusPass, id=pk)
        email = obj.user.email
        name = obj.name

    elif model == 'regular':
        obj = get_object_or_404(RegularBusPass, id=pk)
        email = obj.user.email
        name = obj.name

    elif model == 'renewal':
        obj = get_object_or_404(RenewalRequest, id=pk)
        buspass = (obj.student_pass if obj.pass_type =='Student' else obj.regular_pass)
        email = obj.user.email
        name = buspass.name

    else:
        messages.error(request, "Invalid request")
        return redirect('officer_dashboard')

    if request.method == "POST":
        reason = request.POST.get('reason')

        try:
            send_mail(
                "Bus Pass Request Rejected",
                f"Dear {name},\n\n"
                "Your bus pass request has been rejected.\n\n"
                f"Reason:\n{reason}\n\n"
                "Thank you.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            obj.status = 'Rejected'
            obj.rejection_reason = reason
            obj.save()

            messages.success(request, "Request rejected & mail sent")
            return redirect('officer_dashboard')

        except Exception:
            messages.error(request, "Email could not be sent, Check your internet. Request was not rejected.")

    return render(request, 'officer/reason.html')



