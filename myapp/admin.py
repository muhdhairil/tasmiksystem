from django.contrib import admin
from .models import Teacher, Student, Activity


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_name', 'teacher_email', 'teacher_department', 'teacher_phone')
    search_fields = ('teacher_name', 'teacher_email')
    list_filter = ('teacher_department',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_name', 'student_email', 'student_phone', 'student_program', 'student_class', 'student_sem')
    search_fields = ('student_name', 'student_email')
    list_filter = ('student_program', 'student_class')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'activity_type', 'page', 'date', 'approved')
    list_filter = ('activity_type', 'approved', 'date')
    search_fields = ('student__name', 'teacher__name', 'activity_type')
    ordering = ('-date',)
    


