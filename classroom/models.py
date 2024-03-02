import random
from string import ascii_lowercase

from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User

import misaka

from django.contrib.auth import get_user_model

User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag

from django import template

register = template.Library()


class Classroom(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.CharField(max_length=255, default='')
    slug = models.SlugField(allow_unicode=True, unique=True)
    course = models.TextField(blank=True, default='')
    course_html = models.TextField(editable=False, default='', blank=True)
    code = models.CharField(max_length=255,editable=False)
    members = models.ManyToManyField(User,editable=True, through="ClassMember", related_name='members')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = "".join([random.choice(ascii_lowercase) for _ in range(7)])
        self.slug = slugify(self.name)
        self.course_html = misaka.html(self.course)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("classroom:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class ClassMember(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, related_name='user_classrooms', on_delete=models.CASCADE)
    role = models.CharField(max_length=56, editable=True)

    def __str__(self):
        return self.user.username
    class Meta:
        unique_together = ("classroom", "user")





