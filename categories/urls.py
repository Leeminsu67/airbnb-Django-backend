from django.urls import path
from . import views


urlpatterns = [
    # as_view가 하는 일은 해당 클래스에 GET 메서드이면 get함수 실행 POST이면 post함수 실행하는 역할
    path("", views.Categories.as_view()),
    path("<int:pk>/", views.CategoryDetail.as_view()),
]
