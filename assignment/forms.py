from django import forms
from .models import Assignment



class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class AssignmentForm(forms.ModelForm):
    class Meta:
        fields = ("title", "description", "points", "due")
        model = Assignment
        widgets = {
            'due': DateInput(),
        }
