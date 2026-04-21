from django.urls import path
from . import views

urlpatterns = [
    path('', views.officer_dashboard, name='officer_dashboard'),

    path('new-apply/', views.new_apply_pending_list, name='new_apply_pending_list'),
    path('renewal/', views.renewal_pending_list, name='renewal_pending_list'),

    path('student/approve/<int:pk>/', views.approve_student, name='approve_student'),
    path('regular/approve/<int:pk>/', views.approve_regular, name='approve_regular'),

    path('renewal/approve/<int:pk>/', views.approve_renewal, name='approve_renewal'),

    path('reject/<str:model>/<int:pk>/', views.reject_with_reason, name='reject_with_reason'),
]
