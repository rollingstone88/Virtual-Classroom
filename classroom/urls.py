from django.urls import path

from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.ListClassrooms.as_view(), name="all"),
    path('create/', views.CreateClassroom.as_view(), name="create"),
    path('class/in/<slug>', views.SingleClassroom.as_view(), name="single"),
    path('leave/<slug>', views.LeaveGroup.as_view(), name="leave"),
]
