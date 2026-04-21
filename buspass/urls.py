from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.user_home, name='user_home'),

    path('apply/', views.new_apply, name='new_apply'),
    path('apply/select/', views.select_pass_type, name='select_pass_type'),
    path('student/apply/', views.student_apply, name='student_apply'),
    path('regular/apply/', views.regular_apply, name='regular_apply'),

    path('view/', views.view_buspass, name='view_buspass'),

    path('renewal/', views.renewal_request, name='renewal_request'),

    path('student/epass/<uuid:token>/',views.student_epass,name='student_epass'),
    path('regular/epass/<uuid:token>/',views.regular_epass,name='regular_epass'),
]
