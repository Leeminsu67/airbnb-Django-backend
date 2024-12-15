from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_rooms),
    # 꺽쇠를 열어주고 parameter의 타입을 적어준 다음에 꺽쇠를 닫으면 된다
    # 장고가 url에 있는 타입을 확인해준다.
    path("<int:room_pk>/", views.see_one_room),
]
