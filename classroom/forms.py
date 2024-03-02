from django import forms
from . import models


class ClassroomForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = models.Classroom



