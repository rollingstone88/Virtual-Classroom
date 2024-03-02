from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),

    path('lobby/get_token/', views.getToken),
    #path('lobby/get_room_name/', views.getRoomName),

    path('room/create_member/', views.createMember),
    path('room/get_member/', views.getMember),
    path('room/delete_member/', views.deleteMember),
]