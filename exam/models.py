from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from classroom.models import Classroom


# Create your models here.

class ExamQuestion(models.Model):
    question = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    option1 = models.CharField(max_length=10)
    option2 = models.CharField(max_length=10)
    option3 = models.CharField(max_length=10)
    option4 = models.CharField(max_length=10)
    mark = models.IntegerField()
    ANSWER_CHOICES = (
        ("option1", option1),
        ("option2", option2),
        ("option3", option3),
        ("option4", option4),
    )
    Answer = models.CharField(
        max_length=10,
        choices=ANSWER_CHOICES,
    )

    def __str__(self):
        return f'Question No.{self.id}: {self.question} \t\t Options: \nA. {self.option1} \nB.{self.option2} \nC.{self.option3} \nD.{self.option4} '


class Question_Paper(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    qPaperTitle = models.CharField(max_length=100)
    questions = models.ManyToManyField(ExamQuestion)

    def __str__(self):
        return f' Question Paper Title :- {self.qPaperTitle}\n'


class Exam(models.Model):
    name = models.CharField(max_length=100)
    Qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_marks = models.IntegerField()

    def __str__(self):
        return self.name


class Stu_Question(ExamQuestion):
    teacher = None
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="5")

    def __str__(self):
        return str(self.student.username) + " " + "-Stu_QuestionDB"


class StuExam_DB(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    examname = models.CharField(max_length=100)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Stu_Question)
    score = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student.username) + " " + str(self.examname) + " " + str(
            self.qpaper.qPaperTitle) + "-StuExam_DB"


class StuResults_DB(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exams = models.ManyToManyField(StuExam_DB)

    def __str__(self):
        return str(self.student.username) + " -StuResults_DB"
