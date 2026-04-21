from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime
from .models import StudentBusPass, RegularBusPass, RenewalRequest


# user home

@login_required
def user_home(request):
    return render(request, 'buspass/user_home.html') 

# new apply

@login_required
def new_apply(request):
    return redirect('select_pass_type')

# select pass type

@login_required
def select_pass_type(request):
    return render(request, 'buspass/select_pass_type.html')

# student apply

@login_required
def student_apply(request):
    if request.method == "POST":
        dob_str = request.POST.get('dob')

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        except (ValueError, TypeError):
            messages.error(request,"Invalid date format. Please select a valid date.")
            return redirect('student_apply')

        StudentBusPass.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            dob=dob,
            location=request.POST.get('location'),
            college_id_number=request.POST.get('college_id_number'),
            route_from=request.POST.get('route_from'),
            route_to=request.POST.get('route_to'),
            user_photo=request.FILES.get('user_photo'),
            college_id_image=request.FILES.get('college_id_image'),
        )

        messages.success(request,"Student bus pass application submitted successfully. ""Please wait for verification.")
        return redirect('user_home')

    return render(request, 'buspass/student_apply.html')


# regular apply

@login_required
def regular_apply(request,):
    if request.method == "POST":
        dob_str = request.POST.get('dob')

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request,"Invalid date format. Please select a valid date.")
            return redirect('regular_apply')

        RegularBusPass.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            dob=dob,
            location=request.POST.get('location'),
            user_photo=request.FILES.get('user_photo'),
            aadhar_image=request.FILES.get('aadhar_image'),
        )

        messages.success(request,"Regular bus pass application submitted successfully. ""Please wait for verification.")
        return redirect('user_home')

    return render(request, 'buspass/regular_apply.html')

# view bus pass

@login_required
def view_buspass(request):
    if request.method == "POST":
        epass_id = request.POST.get("pass_id", "").strip()

        if not epass_id:
            messages.error(request, "Please enter a valid E-Pass ID")
            return redirect('view_buspass')

        student = StudentBusPass.objects.filter(epass_id=epass_id,).first()

        if student:
            return redirect('student_epass', token=student.payment_token)

        regular = RegularBusPass.objects.filter(epass_id=epass_id,).first()

        if regular:
            return redirect('regular_epass', token=regular.payment_token)

        messages.error(request,"Bus pass not found")
        return redirect('view_buspass')

    return render(request, 'buspass/view_buspass.html')



# student epass

@login_required
def student_epass(request, token):
    app = get_object_or_404(StudentBusPass, payment_token=token)
    return render(request,"buspass/e_pass.html",{"app": app, "pass_type": "Student"})


# regular epass

@login_required
def regular_epass(request, token):
    app = get_object_or_404(RegularBusPass, payment_token=token)
    return render(request,"buspass/e_pass.html",{"app": app, "pass_type": "Regular"})


# renewal request

@login_required
def renewal_request(request):
    if request.method == "POST":
        epass_id = request.POST.get("pass_id", "").strip()
        if not epass_id:
            messages.error(request, "Please enter E-Pass ID")
            return redirect('renewal_request')

        student = StudentBusPass.objects.filter(epass_id=epass_id).first()

        regular = RegularBusPass.objects.filter(epass_id=epass_id).first()

        if not student and not regular:
            messages.error(request, "Invalid E-Pass ID")
            return redirect('renewal_request')

        buspass = student or regular

        if buspass.expiry_date >= now().date():
                messages.error(request,"Bus pass is not expired yet. Renewal not allowed.")
                return redirect('renewal_request')


        if RenewalRequest.objects.filter(payment_token2=buspass.payment_token).exists():

            if RenewalRequest.objects.filter(payment_token2=buspass.payment_token,status='Pending',).exists():
                messages.warning(request,"Renewal request already submitted.")
                return redirect('renewal_request')

            elif RenewalRequest.objects.filter(payment_token2=buspass.payment_token,status='Approved',).exists():
                messages.warning(request,"The request already approved. check your email for payment page.")
                return redirect('renewal_request')
        
            elif RenewalRequest.objects.filter(payment_token2=buspass.payment_token,status='Rejected',).exists():
                messages.warning(request,"Your request rejected. check your email for rejection reason.")
                return redirect('renewal_request')

            # -----

            not_new_user = RenewalRequest.objects.filter(payment_token2=buspass.payment_token,status='Completed').first()
            if not_new_user:
                not_new_user.status = 'Pending'
                not_new_user.save()
            
        else:
            RenewalRequest.objects.create(
                user=buspass.user,
                pass_type='Student' if student else 'Regular',
                student_pass=student,
                regular_pass=regular,
                status='Pending',
                payment_token2=buspass.payment_token
            )
                
        messages.success(request,"Renewal request sent successfully. ""Please wait for verification.")
        return redirect('user_home')

    return render(request, 'buspass/renewal.html')
