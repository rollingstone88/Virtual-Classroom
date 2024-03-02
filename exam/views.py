import threading
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from classroom.models import Classroom, ClassMember
from . import models
from . import forms
# Create your views here.
from django.views import generic, View
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage


class AddQuestion(LoginRequiredMixin, generic.CreateView):
    model = models.ExamQuestion
    form_class = forms.QForm
    template_name = "exam/addquestions.html"

    def get_success_url(self):
        return reverse_lazy("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_form = forms.QForm(self.request.POST)
        context["exam_form"] = exam_form
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        context["classroom"] = classroom
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        self.object.classroom = classroom
        self.object.save()
        return super().form_valid(form)


class AddQuestionPaper(LoginRequiredMixin, generic.CreateView):
    model = models.Question_Paper
    form_class = forms.QPForm
    template_name = "exam/addquestionpaper.html"

    def get_form_kwargs(self):
        kwargs = super(AddQuestionPaper, self).get_form_kwargs()
        kwargs['teacher'] = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        kwargs['classroom'] = classroom
        return kwargs

    def get_success_url(self):
        return reverse_lazy("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        exam_form = forms.QPForm(teacher, classroom, self.request.POST)
        context["exam_form"] = exam_form
        context["classroom"] = classroom
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        self.object.classroom = classroom
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class CreateExam(LoginRequiredMixin, generic.CreateView):
    model = models.Exam
    form_class = forms.ExamForm
    template_name = "exam/create_exam.html"

    def get_success_url(self):
        return reverse_lazy("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def get_form_kwargs(self):
        kwargs = super(CreateExam, self).get_form_kwargs()
        kwargs['teacher'] = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        kwargs['classroom'] = classroom
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        exam_form = forms.ExamForm(teacher, classroom, self.request.POST)
        context["exam_form"] = exam_form
        context["classroom"] = classroom
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher = self.request.user
        classroom = Classroom.objects.get(slug=self.kwargs.get("slug"))
        self.object.classroom = classroom
        questions = self.object.Qpaper.questions.all()
        self.object.total_marks = 0
        for q in questions:
            self.object.total_marks += q.mark

        self.object.save()
        return super().form_valid(form)


@login_required(login_url='login')
def view_exams_student(request, code):
    classroom = Classroom.objects.get(code=code)
    exams = models.Exam.objects.filter(classroom=classroom)
    list_of_completed = []
    list_un = []
    for exam in exams:
        if models.StuExam_DB.objects.filter(examname=exam.name, student=request.user).exists():
            if models.StuExam_DB.objects.get(examname=exam.name, student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            IST = pytz.timezone('Asia/Dhaka')
            if exam.end_time > datetime.now(IST):
                list_un.append(exam)

    return render(request, 'exam/student_view_exam.html', {
        'exams': list_un,
        'completed': list_of_completed,
        'classroom': classroom,
    })


def student_view_previous(request, slug):
    classroom = Classroom.objects.get(slug=slug)
    exams = models.Exam.objects.filter(classroom=classroom)
    list_of_completed = []
    list_un = []
    for exam in exams:
        if models.StuExam_DB.objects.filter(examname=exam.name, student=request.user).exists():
            if models.StuExam_DB.objects.get(examname=exam.name, student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request, 'exam/student_previous_exams.html', {
        'exams': list_un,
        'completed': list_of_completed,
        'classroom': classroom,
    })


@login_required(login_url='login')
def view_students_teacher(request, code):
    classroom = Classroom.objects.get(code=code)
    students = classroom.members.all()
    student_name = []
    student_completed = []
    dicts = {}
    examn = models.Exam.objects.filter(teacher=request.user, classroom=classroom)
    for student in students:
        user_role = ClassMember.objects.get(user=student, classroom=classroom).role
        print(user_role)
        if user_role == 'student':
            student_name.append(student.username)
            count = 0
            for exam in examn:
                if models.StuExam_DB.objects.filter(student=student, examname=exam.name, completed=1).exists():
                    count += 1
                else:
                    count += 0
            student_completed.append(count)
            i = 0
            for x in student_name:
                dicts[x] = student_completed[i]
                i += 1

    return render(request, 'exam/viewstudents.html', {
        'students': dicts,
        'classroom': classroom,
    })


@login_required(login_url='faculty-login')
def view_results_teacher(request, code):
    classroom = Classroom.objects.get(code=code)
    dicts = {}
    teacher = request.user

    examn = models.Exam.objects.filter(teacher=teacher, classroom=classroom)
    for exam in examn:
        if models.StuExam_DB.objects.filter(examname=exam.name, completed=1).exists():
            students_filter = models.StuExam_DB.objects.filter(examname=exam.name, completed=1)
            for student in students_filter:
                key = str(student.student) + " " + str(student.examname) + " " + str(student.qpaper.qPaperTitle)
                dicts[key] = student.score
    return render(request, 'exam/resultsstudent.html', {
        'students': dicts,
        'classroom': classroom,
    })


@login_required(login_url='faculty-login')
def view_previousexams_teacher(request, code):
    classroom = Classroom.objects.get(code=code)
    prof = request.user
    student = 0
    exams = models.Exam.objects.filter(classroom=classroom)
    return render(request, 'exam/teacher_view_previousexam.html', {
        'exams': exams, 'prof': prof,
        'classroom': classroom,
    })


@login_required(login_url='login')
def view_students_attendance(request, code):
    classroom = Classroom.objects.get(code=code)
    exams = models.Exam.objects.filter(classroom=classroom)
    list_of_completed = []
    list_un = []
    for exam in exams:
        if models.StuExam_DB.objects.filter(examname=exam.name, student=request.user).exists():
            if models.StuExam_DB.objects.get(examname=exam.name, student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            IST = pytz.timezone('Asia/Dhaka')
            if exam.end_time < datetime.now(IST):
                list_un.append(exam)

    return render(request, 'exam/attendance.html', {
        'exams': list_un,
        'completed': list_of_completed,
        'classroom': classroom,
    })


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    min += hour * 60
    return "%02d:%02d" % (min, sec)


@login_required(login_url='login')
def appear_exam(request, id):
    student = request.user
    if request.method == 'GET':
        exam = models.Exam.objects.get(pk=id)
        classroom = exam.classroom

        IST = pytz.timezone('Asia/Dhaka')

        time_left = datetime.now(IST) - exam.start_time
        time_adjusted = datetime.now(IST) - timedelta(hours=6)

        time_left1 = datetime.now(timezone.utc) - exam.start_time
        time_left2 = exam.start_time - datetime.now(timezone.utc)

        print(datetime.now(IST))
        print(exam.start_time)
        print(exam.start_time - datetime.now(IST))
        print(datetime.now(IST) - exam.start_time)

        cont = {
            'classroom': classroom
        }
        if exam.start_time > datetime.now(IST):
            return render(request, 'exam/Prior_to_exam.html', cont)

        if exam.end_time < datetime.now(IST):
            return render(request, 'exam/after_ending_time.html', cont)

        if exam.start_time < datetime.now(IST) <= exam.end_time:
            time_delta = exam.end_time - datetime.now(IST)
        else:
            time_delta = exam.end_time - exam.start_time

        time = convert(time_delta.seconds)
        time = time.split(":")
        mins = time[0]
        secs = time[1]
        context = {
            "exam": exam,
            "question_list": exam.Qpaper.questions.all(),
            "secs": secs,
            "mins": mins,
            'classroom': classroom,
        }
        return render(request, 'exam/giveExam.html', context)
    if request.method == 'POST':
        student = User.objects.get(username=request.user.username)
        paper = request.POST['paper']
        exam_id = request.POST['exam_id']
        examMain = models.Exam.objects.get(id=exam_id)
        stuExam = models.StuExam_DB.objects.get_or_create(examname=paper, student=student, qpaper=examMain.Qpaper)[0]

        qPaper = examMain.Qpaper
        stuExam.qpaper = qPaper
        classroom = examMain.classroom

        qPaperQuestionsList = examMain.Qpaper.questions.all()
        for ques in qPaperQuestionsList:
            student_question = models.Stu_Question(student=student, classroom=classroom, question=ques.question,
                                                   option1=ques.option1,
                                                   option2=ques.option2, option3=ques.option3, option4=ques.option4,
                                                   Answer=ques.Answer, mark=ques.mark)
            student_question.save()
            stuExam.questions.add(student_question)
            stuExam.save()

        stuExam.completed = 1
        stuExam.save()
        examQuestionsList = \
            models.StuExam_DB.objects.filter(student=request.user, examname=paper, qpaper=examMain.Qpaper,
                                             questions__student=request.user)[0]
        # examQuestionsList = stuExam.questions.all()
        examScore = 0
        list_i = examMain.Qpaper.questions.all()
        queslist = examQuestionsList.questions.all()
        i = 0
        for j in range(list_i.count()):
            ques = queslist[j]
            max_m = list_i[i].mark
            ans = request.POST.get(ques.question, False)

            if not ans:
                ans = "5"
            ques.choice = ans
            ques.save()

            option = {
                '1': "option1",
                '2': "option2",
                '3': "option3",
                '4': "option4",
                '5': 'notFound',
            }

            print(ans)
            print(ques.Answer)
            print(ans)
            print(ques.Answer)

            if option[ans] == ques.Answer:
                examScore = examScore + max_m
            i += 1

        stuExam.score = examScore
        stuExam.save()
        stu = models.StuExam_DB.objects.filter(student=request.user, examname=examMain.name)
        results = models.StuResults_DB.objects.get_or_create(student=request.user)[0]
        results.exams.add(stu[0])
        results.save()

        return redirect('exam:view_exams_student', code=classroom.code)


@login_required(login_url='login')
def result(request, id):
    student = request.user
    exam = models.Exam.objects.get(pk=id)
    score = models.StuExam_DB.objects.get(student=student, examname=exam.name, qpaper=exam.Qpaper).score
    return render(request, 'exam/result.html', {'exam': exam, "score": score, "classroom": exam.classroom})


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)
