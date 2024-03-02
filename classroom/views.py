import random
from string import ascii_lowercase

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import Http404, JsonResponse

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import TemplateView

from classroom.models import Classroom, ClassMember
from . import models

from classroom.forms import ClassroomForm

User = get_user_model()

def random_str(digit=7):
    return "".join([random.choice(ascii_lowercase) for _ in range(digit)])

class CreateClassroom(LoginRequiredMixin, generic.CreateView):
    model = Classroom
    fields = ("name", "description")
    model.code = random_str()

    def get_initial(self, *args, **kwargs):
        initial = super(CreateClassroom, self).get_initial(**kwargs)
        initial['code'] = random_str()
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        ClassMember.objects.create(user=self.request.user, classroom=self.object, role='teacher')
        return super().form_valid(form)


class SingleClassroom(generic.DetailView):
    model = Classroom

    def get_context_data(self, **kwargs):
        class_member = ClassMember.objects.get(user=self.request.user, classroom=self.object)
        user_role = class_member.role
        context = super().get_context_data(**kwargs)
        context["user_role_in_classroom"] = user_role
        return context


class ListClassrooms(generic.ListView):
    model = Classroom


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            membership = models.ClassMember.objects.filter(
                user=self.request.user,
                classroom__slug=self.kwargs.get("slug")
            ).get()

        except models.ClassMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)


