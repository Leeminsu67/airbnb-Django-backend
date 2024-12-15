from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    """
    3개의 매개변수가 필요하다는건 꼭 기억해야함
    첫번째는 이 액션을 호출한 클래스인 model_admin
    두번째는 이 액션을 호출한 유저 정보를 가지고 있는 request 객체
    세번째는 queryset인데 내가 마음대로 이름을 정할 수 있음
    """
    for room in rooms:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
        "rating",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    # FK된 사용자의 이름으로 방을 검색하고 싶음
    search_fields = (
        # "name",
        # "price", __contains를 검색어를 포함하고 있는 방을 찾음
        # "^price", __statswith를 검색어를 첫 글자부터
        # "=price", 검색어와 100% 동일한 값만 보여줌
        # "price",
        "=owner__username",
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
