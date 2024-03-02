from django.contrib import admin
from .models import Exam, Question_Paper, ExamQuestion, StuExam_DB, Stu_Question, StuResults_DB

# Register your models here.
admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(Question_Paper)
admin.site.register(Stu_Question)
admin.site.register(StuResults_DB)
admin.site.register(StuExam_DB)

