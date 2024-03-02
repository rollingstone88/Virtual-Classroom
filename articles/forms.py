from django import forms
from . import models


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=9999)
    comment_image = forms.ImageField()
