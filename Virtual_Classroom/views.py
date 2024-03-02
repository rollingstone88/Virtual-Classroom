from pyexpat.errors import messages

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from classroom import models
from classroom.models import Classroom, ClassMember


class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = 'index.html'


class JoinClassroom(TemplateView):
    template_name = 'join_classroom.html'


def joinClassroom(request):
    classroomCode = request.POST['classroom_code']

    try:
        classroom = Classroom.objects.get(code=classroomCode)
        ClassMember.objects.create(user=request.user, classroom=classroom, role='student')
        return render(request, "thanks.html")
    except:
        print("error joining")
        return render(request, "NoClassroomFound.html")
