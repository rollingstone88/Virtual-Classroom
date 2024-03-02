from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from . import models


class QForm(ModelForm):
    class Meta:
        model = models.ExamQuestion
        fields = '__all__'
        exclude = ['teacher', 'classroom']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'optionA': forms.TextInput(attrs={'class': 'form-control'}),
            'optionB': forms.TextInput(attrs={'class': 'form-control'}),
            'optionC': forms.TextInput(attrs={'class': 'form-control'}),
            'optionD': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class QPForm(ModelForm):
    def __init__(self, teacher, classroom, *args, **kwargs):
        super(QPForm, self).__init__(*args, **kwargs)
        self.fields['questions'].queryset = models.ExamQuestion.objects.filter(
            teacher=teacher, classroom=classroom)

    class Meta:
        model = models.Question_Paper
        fields = '__all__'
        exclude = ['teacher', 'classroom']
        widgets = {
            'QuestionPaperTitle': forms.TextInput(attrs={'class': 'form-control'}),
            'Questions': forms.TextInput(attrs={'class': 'form-control'})
        }


class ExamForm(ModelForm):
    def __init__(self, teacher, classroom, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['Qpaper'].queryset = models.Question_Paper.objects.filter(teacher=teacher,

                                                                              classroom=classroom)

    class Meta:
        model = models.Exam
        fields = '__all__'
        exclude = ['teacher', 'classroom', 'total_marks']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
