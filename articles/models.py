from django.db import models
from classroom.models import Classroom
from django.contrib.auth.models import User


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="articles")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="articles")
    assign_time = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)


class ArticleComment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="comment")
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comment")
    comment_text = models.TextField()
    comment_image = models.FileField(upload_to='comment', blank=True, null=True)
    comment_time = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment")
