from django.contrib import admin
from .models import StudentBusPass, RegularBusPass, RenewalRequest

# Register your models here.

admin.site.register(StudentBusPass)
admin.site.register(RegularBusPass)
admin.site.register(RenewalRequest)
