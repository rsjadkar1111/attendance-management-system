from django.contrib import admin
from .models import Student, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'department', 'year', 'created_at']
    list_filter = ['department', 'year']
    search_fields = ['roll_number', 'name', 'email']
    ordering = ['roll_number']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'remarks', 'marked_at']
    list_filter = ['date', 'status']
    search_fields = ['student__roll_number', 'student__name']
    date_hierarchy = 'date'
    ordering = ['-date', 'student__roll_number']
