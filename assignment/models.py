from django.db import models
from classroom.models import Classroom
from django.contrib.auth.models import User


# Create your models here.

class Assignment(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="assignments")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="assignments")
    assign_time = models.DateTimeField(auto_now=True)
    due = models.DateTimeField()
    points = models.IntegerField()


class AssignmentSubmission(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="submission")
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="submission")
    file = models.FileField(upload_to='media')
    submission_time = models.DateTimeField(auto_now=True)
    turn_in_status = models.CharField(max_length=10, default="timely")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submission")

    def __str__(self):
        return f' Assignment Submission for :- {self.assignment} by {self.student.username} \t\t\n'


class AssignmentComment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="assignment_comment")
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="assignment_comment")
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="assignment_comment")
