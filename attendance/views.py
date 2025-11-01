from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
from .models import Student, Attendance


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'attendance/login.html')


@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    students = Student.objects.all()
    total_students = students.count()
    
    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='Present').count()
    absent_today = today_attendance.filter(status='Absent').count()
    
    recent_attendance = Attendance.objects.all()[:10]
    
    attendance_summary = []
    for student in students:
        total_days = student.attendances.count()
        present_days = student.attendances.filter(status='Present').count()
        percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        attendance_summary.append({
            'student': student,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': total_days - present_days,
            'percentage': round(percentage, 2)
        })
    
    context = {
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'recent_attendance': recent_attendance,
        'attendance_summary': attendance_summary,
        'today': today,
    }
    return render(request, 'attendance/dashboard.html', context)


@login_required
def add_student(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        year = request.POST.get('year')
        
        try:
            student = Student.objects.create(
                roll_number=roll_number,
                name=name,
                email=email,
                phone=phone,
                department=department,
                year=year
            )
            messages.success(request, f'Student {student.name} added successfully!')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    return render(request, 'attendance/add_student.html')


@login_required
def student_list(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'attendance/student_list.html', context)


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        attendance_date = request.POST.get('date')
        
        if not attendance_date:
            messages.error(request, 'Please select a date.')
            return redirect('mark_attendance')
        
        students = Student.objects.all()
        marked_count = 0
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={'status': status, 'remarks': remarks}
                )
                marked_count += 1
        
        messages.success(request, f'Attendance marked for {marked_count} students on {attendance_date}.')
        return redirect('dashboard')
    
    students = Student.objects.all()
    today = date.today()
    context = {
        'students': students,
        'today': today,
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def attendance_records(request):
    attendances = Attendance.objects.all()
    
    selected_date = request.GET.get('date')
    if selected_date:
        attendances = attendances.filter(date=selected_date)
    
    context = {
        'attendances': attendances,
        'selected_date': selected_date,
    }
    return render(request, 'attendance/attendance_records.html', context)
