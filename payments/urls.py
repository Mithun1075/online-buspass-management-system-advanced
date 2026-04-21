from django.urls import path
from . import views

urlpatterns = [
    # new apply payment
    path('student/<uuid:token>/', views.student_payment, name='student_payment'),
    path('regular/<uuid:token>/', views.regular_payment, name='regular_payment'),

    # renewal payments
    path('renewal/student/<uuid:renewal_id>/', views.student_renewal_payment, name='student_renewal_payment'),
    path('renewal/regular/<uuid:renewal_id>/', views.regular_renewal_payment, name='regular_renewal_payment'),
]