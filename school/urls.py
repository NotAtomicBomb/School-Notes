from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('question/<int:question_id>/results/', views.results, name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    path('school/', views.school_index, name='school'),
    path('school/<str:course_id>/', views.course_subjects, name='subjects'),
    path('school/<str:course_id>/<str:subject_name>', views.course_subject, name='subject')
]
