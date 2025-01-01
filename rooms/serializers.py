from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


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

    class Meta:
        model = Room
        fields = "__all__"

    # 무조건 get을 붙여줘야하고 get_속성값
    def get_rating(self, room):
        return room.rating()


class RoomSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()

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
        )

    def get_rating(self, room):
        return room.rating()
