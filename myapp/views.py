import requests
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.cache import cache  # Import cache module
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, StudentForm, TeacherForm, LoginForm
from .models import Student, Teacher, Activity
from django.db.models import Count



def surah_list(request):
    response = requests.get('http://api.alquran.cloud/v1/surah')
    if response.status_code == 200:
        data = response.json()
        surahs = data.get('data', [])
    else:
        surahs = []
    return render(request, 'surahlist.html', {'surahs': surahs})

def surah_detail(request, surah_number, editions):
    url = f'http://api.alquran.cloud/v1/surah/{surah_number}/editions/{editions}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        surah_editions = data.get('data', [])
    else:
        surah_editions = []
    return render(request, 'surahdetail.html', {'surah_editions': surah_editions})


def quran_edition(request, edition):
    quran_cache_key = f'quran_{edition}'
    quran = cache.get(quran_cache_key)  # Try to get data from cache first

    if quran is None:  # If data is not found in cache, fetch from API
        try:
            url = f'http://api.alquran.cloud/v1/quran/{edition}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                quran = data.get('data', {})
                # Store data in cache for future use
                cache.set(quran_cache_key, quran, timeout=3600)  # Cache for 1 hour
            else:
                quran = {}
        except requests.RequestException as e:
            # Handle request exceptions
            quran = {}

    return render(request, 'quranedition.html', {'quran': quran})

def quran_page(request, page, edition):
    url = f'http://api.alquran.cloud/v1/page/{page}/{edition}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        page_data = data.get('data', {})
    else:
        page_data = {}
        
    teachers = Teacher.objects.all()
        
    return render(request, 'quranpage.html', {'page_data': page_data, 'teachers': teachers})  


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Store custom session data
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                
                # Determine if the user is a student or teacher and store additional data
                try:
                    student = Student.objects.get(id=user.id)
                    request.session['role'] = 'student'
                    request.session['full_name'] = student.student_name
                except Student.DoesNotExist:
                    try:
                        teacher = Teacher.objects.get(id=user.id)
                        request.session['role'] = 'teacher'
                        request.session['full_name'] = teacher.teacher_name
                    except Teacher.DoesNotExist:
                        request.session['role'] = 'unknown'

                return redirect('home')  # Redirect to a home page or any other page
            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

def choose_signup(request):
    return render(request, 'choose_signup.html')

def register_user(request, role):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if role == 'student':
            specific_form = StudentForm(request.POST)
        else:  # role is 'teacher'
            specific_form = TeacherForm(request.POST)

        if user_form.is_valid() and specific_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            if role == 'teacher':
                user.is_superuser = True
                user.is_staff = True
                user.save()
                teacher_instance = Teacher(user=user,
                                           id = user.id,
                                           teacher_name=specific_form.cleaned_data['teacher_name'],
                                           teacher_email=user.email,
                                           teacher_department=specific_form.cleaned_data['teacher_department'],
                                           teacher_phone=specific_form.cleaned_data['teacher_phone'])
                teacher_instance.save()
            else:
                student_instance = Student(user=user,
                                           id = user.id,
                                           student_name=specific_form.cleaned_data['student_name'],
                                           student_email=user.email,
                                           student_program=specific_form.cleaned_data['student_program'],
                                           student_class=specific_form.cleaned_data['student_class'],
                                           student_phone=specific_form.cleaned_data['student_phone'],
                                           student_sem =specific_form.cleaned_data['student_sem'])
                                           
                student_instance.save()

            login(request, user)
            return redirect('login')  # Redirect to login or any other page after successful registration

    else:
        user_form = UserForm()
        if role == 'student':
            specific_form = StudentForm()
        else:  # role is 'teacher'
            specific_form = TeacherForm()

    return render(request, 'register_user.html', {
        'user_form': user_form,
        'specific_form': specific_form,
        'role': role
    })
    
def home(request):

    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    username = user.username
    
    if user.is_superuser:
        teacher = get_object_or_404(Teacher, id=user_id)
        full_name = teacher.teacher_name
    else:
        role ='student'
        student = get_object_or_404(Student, id=user_id)
        full_name = student.student_name
        

    context = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'full_name': full_name,
    }
    return render(request, 'homepage.html', context)

def teacher_activity(request):
    if request.user.is_authenticated and request.user.is_superuser:
        teacher_id = request.user.id
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        activities = Activity.objects.filter(teacher=teacher)
        return render(request, 'teacher_activity.html', {'activities': activities})
    else:
        return redirect('home')
    
def update_approval(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        approved = request.POST.get('approved', False)
        activity.approved = bool(approved)
        activity.save()
    return redirect('teacher_activity')

def activity(request, activity_type, page_number=None):
    if request.method == 'POST':
        page_number = request.POST.get('page_number', 1)
    elif request.method == 'GET' and 'page_number' in request.GET:
        page_number = request.GET.get('page_number')

    if page_number is None:
        page_number = 1

    url = f'http://api.alquran.cloud/v1/page/{page_number}/quran-uthmani'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        page_data = data.get('data', {})
    else:
        page_data = {}

    teachers = Teacher.objects.all()
    

    return render(request, 'activity_page.html', {
        'activity_type': activity_type,
        'page_data': page_data,
        'teachers': teachers,
        'page_number': int(page_number)
    })
 

def choose_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        student_id = request.session.get('user_id')
        tasmik_page = request.POST.get('page_data')
        activity_type = request.POST.get('activity_type')

        current_time = timezone.now()
        
        # Retrieve the Student and Teacher instances
        student = Student.objects.get(id=student_id)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        
        tasmik = Activity.objects.create(
            activity_type=activity_type,
            student=student,
            teacher=teacher,
            page=tasmik_page, 
            date=current_time 
        )
        
        return redirect('home')
    
    return redirect('home')

def record_view(request):
    student_id = request.user.id
    student = get_object_or_404(Student, pk=student_id)
    activities = Activity.objects.filter(student=student)
    return render(request, 'record.html', {'activities': activities})

def semester_buttons_view(request):
    if not request.user.is_superuser:  # Ensure only teachers access this view
        return redirect('home')
    return render(request, 'semester_buttons.html')

def student_records_by_semester(request, sem):
    if not request.user.is_superuser:  # Ensure only teachers access this view
        return redirect('home')

    students = Student.objects.filter(student_sem=sem)

    approved_activities = Activity.objects.filter(student__student_sem=sem, approved=True).values('student', 'page').annotate(count=Count('id'))
    pending_activities = Activity.objects.filter(student__student_sem=sem, approved=None).values('student', 'page').annotate(count=Count('id'))
    
    approved_activities_dict = {}
    pending_activities_dict = {}

    for activity in approved_activities:
        student_id = activity['student']
        if student_id not in approved_activities_dict:
            approved_activities_dict[student_id] = []
        approved_activities_dict[student_id].append({'count': activity['count'], 'page': activity['page']})

    for activity in pending_activities:
        student_id = activity['student']
        if student_id not in pending_activities_dict:
            pending_activities_dict[student_id] = []
        pending_activities_dict[student_id].append({'count': activity['count'], 'page': activity['page']})

    context = {
        'students': students,
        'semester': sem,
        'approved_activities_dict': approved_activities_dict,
        'pending_activities_dict': pending_activities_dict,
    }
    return render(request, 'student_records_by_semester.html', context)

