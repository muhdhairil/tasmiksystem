from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('register/<str:role>/', views.register_user, name='register_user'),
    path('choose-signup/', views.choose_signup, name='choose_signup'),
    path('record/', views.record_view, name='record'),
    path('semesters/', views.semester_buttons_view, name='semester_buttons'),
    path('records/semester/<int:sem>/', views.student_records_by_semester, name='student_records_by_semester'),
    path('teacher/activity/', views.teacher_activity, name='teacher_activity'),
    path('update_approval/<int:activity_id>/', views.update_approval, name='update_approval'),
    path('activity/<str:activity_type>/', views.activity, name='activity'),
    path('surahs/', views.surah_list, name='surah_list'),
    path('surah/<int:surah_number>/editions/<str:editions>/', views.surah_detail, name='surah_detail'),
    path('quran/<str:edition>/', views.quran_edition, name='quran_edition'),
    path('quran/page/<int:page>/<str:edition>/', views.quran_page, name='quran_page'),
    path('choose_teacher/', views.choose_teacher, name='choose_teacher'),
]
