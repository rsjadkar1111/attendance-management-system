from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/records/', views.attendance_records, name='attendance_records'),
]
