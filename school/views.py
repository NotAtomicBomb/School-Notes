from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from school.models import Question, Course


# Create your views here.
def school_index(request):
    course_list = get_list_or_404(Course.objects.all())
    return render(request, "school/index.html", {"course_list": course_list})


def course_subjects(request, course_id):
    course = get_object_or_404(Course, course_code=course_id)
    return render(request, 'school/subjects.html', {"course": course})


def index(request):
    latest_question_list = get_list_or_404(Question.objects.order_by('-pub_date').reverse())
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
