from django.urls import path
from . import views

# https://www.django-rest-framework.org/api-guide/viewsets/
# 참고 사이트
urlpatterns = [
    # as_view가 하는 일은 해당 클래스에 GET 메서드이면 get함수 실행 POST이면 post함수 실행하는 역할
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>/",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
