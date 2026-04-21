from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
import uuid
import random


def generate_epass_id():
    return f"EPB-{random.randint(1000, 9999)}"


def one_month_expiry():
    """Expiry date = today + 30 days"""
    return now().date() + timedelta(days=30)


class StudentBusPass(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    epass_id = models.CharField(max_length=10,unique=True,default=generate_epass_id)

    name = models.CharField(max_length=100)
    dob = models.DateField(default="2000-01-01")
    college_id_number = models.CharField(max_length=50)
    location = models.CharField(max_length=150, default="Unknown")
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    user_photo = models.ImageField(upload_to='user_photos/')
    college_id_image = models.ImageField(upload_to='college_ids/')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    applied_date = models.DateTimeField( auto_now_add=True )

    expiry_date = models.DateField(default=one_month_expiry)

    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.epass_id} - {self.name} - {self.status}"


class RegularBusPass(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    epass_id = models.CharField( max_length=10, unique=True, default=generate_epass_id)

    name = models.CharField(max_length=100)
    dob = models.DateField(default="2000-01-01")
    location = models.CharField(max_length=150)

    user_photo = models.ImageField(upload_to='user_photos/')
    aadhar_image = models.ImageField(upload_to='aadhar_cards/')

    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default='Pending')

    applied_date = models.DateTimeField(auto_now_add=True)

  
    expiry_date = models.DateField(default=one_month_expiry)

    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.epass_id} - {self.name} - {self.status}"

class RenewalRequest(models.Model):

    PASS_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Regular', 'Regular'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    pass_type = models.CharField( max_length=10,choices=PASS_TYPE_CHOICES )

    student_pass = models.ForeignKey(StudentBusPass, on_delete=models.CASCADE, null=True, blank=True )
    regular_pass = models.ForeignKey( RegularBusPass, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default='Pending')

    rejection_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    payment_token2 = models.UUIDField(null=True) 

    def __str__(self):
        return f"Renewal - {self.pass_type} - {self.status}"
