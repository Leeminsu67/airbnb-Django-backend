from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    # owner = TinyUserSerializer()
    owner = TinyUserSerializer(read_only=True)
    # 해당 데이터가 배열일경우 many=True 설정 해줘야함
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    # serializer에서 models.py에 있는 메서드를 가져와서 보여주고 싶을때
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # 좋아요를 한 유저가 있는지 확인
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    # 무조건 get을 붙여줘야하고 get_속성값
    def get_rating(self, room):
        return room.rating()

    # 이 방의 주인인지 아닌지 확인
    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()


class RoomSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        # fields = "__all__"
        # FK가 잡혀있고 PK만 나오는 데이터를 다 보여줌
        # 문제점은 커스터마이징을 할 수 없다는 것
        # depth = 1

        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
