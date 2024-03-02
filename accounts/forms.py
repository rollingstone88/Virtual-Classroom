from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birth_date = forms.DateField(required=True, widget=DatePickerInput)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date', 'profile_pic')
        model = get_user_model()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['username'].label = 'Display Name'
            self.fields['email'].label = "Email Address"
