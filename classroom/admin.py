from django.contrib import admin

from . import models


class GroupMemberInline(admin.TabularInline):
    model = models.ClassMember


admin.site.register(models.Classroom)
