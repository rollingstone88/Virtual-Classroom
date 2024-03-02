from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def lobby(request):
    return render(request, 'communication_channel/lobby.html')


def room(request):
    return render(request, 'communication_channel/room.html')

'''
def getRoomName(request):

    room_name = 'CSE-4500'

    return JsonResponse({'room_name': room_name}, safe=False)

'''

def getToken(request):
    appId = "ce751ed63bd4455790025d03f4f26af5"
    appCertificate = "ca1952ccea7c46019d3036eca3af60e5"
    channelName = request.GET.get('channel')
    # uid = random.randint

    #### making login user join channel
    current_user = request.user
    uid = current_user.id
    name = current_user.get_full_name()
    room_name = 'CSE-4500'
    ###

    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid, 'room_name': room_name}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)

    ####
    current_user = request.user
    uid = current_user.id
    name = current_user.get_full_name()
    room_name = "CSE-4500"
    ####

    member, created = RoomMember.objects.get_or_create(
        name=name,
        uid=uid,
        room_name= data['room_name']
    )

    return JsonResponse({'name': name}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    ####
    current_user = request.user
    uid = current_user.id
    name = current_user.get_full_name()
    ####

    member = RoomMember.objects.get(
        name=name,
        uid=uid,
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)