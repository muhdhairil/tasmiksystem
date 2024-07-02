# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'student_phone', 'student_program', 'student_class','student_sem']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_email', 'teacher_department', 'teacher_phone']