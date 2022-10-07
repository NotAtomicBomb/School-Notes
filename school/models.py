import datetime
import os
import shutil

from django.db import models
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subject_name

    def proper_url_name(self):
        return self.subject_name.replace(' ', '-')


@receiver(models.signals.post_save, sender=Subject)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        name = instance.proper_url_name().lower()
        course_name = instance.course.course_code.lower()
        source = 'school/templates/template.html'
        target = f'school/templates/school/subjects/{course_name}/{name}.html'
        shutil.copy(source, target)
        print(instance.course.course_code)


@receiver(models.signals.post_save, sender=Course)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        name = instance.course_code.lower()
        try:
            os.mkdir(f'school/templates/school/subjects/{name}/')
        except:
            print("Directory already exists")


@receiver(models.signals.post_delete, sender=Course)
def execute_after_save(sender, instance, **kwargs):
    name = instance.course_code.lower()
    try:
        os.rmdir(f'school/templates/school/subjects/{name}/')
    except:
        print("Directory already deleted")


@receiver(models.signals.post_delete, sender=Subject)
def execute_after_deletion(sender, instance, **kwargs):
    name = instance.proper_url_name().lower()
    course_name = instance.course.course_code.lower()
    filepath = f'school/templates/school/subjects/{course_name}/{name}.html'
    if os.path.exists(filepath):
        os.remove(filepath)
        print("File was deleted")
    else:
        print("File was already deleted")


@receiver(models.signals.post_init, sender=Subject)
def execute_after_deletion(sender, instance, **kwargs):
    try:
        name = instance.proper_url_name().lower()
        course_name = instance.course.course_code.lower()
        source = 'school/templates/template.html'
        target = f'school/templates/school/subjects/{course_name}/{name}.html'
        if not os.path.exists(target):
            shutil.copy(source, target)
        else:
            print("File already exists")
        print(name)
    except:
        return


@receiver(models.signals.post_init, sender=Course)
def execute_after_deletion(sender, instance, **kwargs):
    course_name = instance.course_code.lower()
    try:
        os.mkdir(f'school/templates/school/subjects/{course_name}/')
    except:
        return
