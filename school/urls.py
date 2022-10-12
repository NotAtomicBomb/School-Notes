from django.urls import path

from . import views

urlpatterns = [
    path('', views.school_index, name='school'),
    path('/<str:course_id>/', views.course_subjects, name='subjects'),
    path('/<str:course_id>/<str:subject_name>', views.course_subject, name='subject')
]
