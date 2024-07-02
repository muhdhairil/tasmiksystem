from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=100)
    teacher_email = models.EmailField(unique=True)
    teacher_department = models.CharField(max_length=100)
    teacher_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.teacher_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_phone = models.CharField(max_length=15)
    student_program = models.CharField(max_length=100)
    student_class = models.CharField(max_length=100)
    student_sem = models.CharField(max_length=15,default=1)

    def __str__(self):
        return self.student_name

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('murajaah', 'Murajaah'),
        ('tasmik', 'Tasmik'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    page = models.IntegerField()
    date = models.DateField()
    approved = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.activity_type.capitalize()} by {self.teacher} for {self.student}"

    def get_approved_display(self):
        if self.approved is None:
            return "Waiting for Verification"
        elif self.approved:
            return "Verified"
        else:
            return "Not Verified"
