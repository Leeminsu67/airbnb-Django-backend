from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# view란 유저가 특정 url에 접근했을때 작동하게 되는 함수
"""
request object는 요청하고 있는 브라우저의 정보, 전송하고 있는 데이터, 요청한 url 정보
ip 주소, 쿠키 등 모든 정보를 가지고 있다.
"""


def see_all_rooms(request):
    rooms = Room.objects.all()
    # return HttpResponse("see all rooms")
    # render의 첫번째 인자로 request를 넘겨주고 해당 앱의 html파일 중 하나를 선택(templates -> html)
    # 세번째는 딕셔너리 형태로 원하는 키값과 넘겨주고 싶은 데이터를 넘겨준다
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django!",
        },
    )


def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        # return HttpResponse(f"see one room: {room_pk}")
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
