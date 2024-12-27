from rest_framework.serializers import ModelSerializer
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
    owner = TinyUserSerializer()
    # 해당 데이터가 배열일경우 many=True 설정 해줘야함
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"


class RoomSerializer(ModelSerializer):
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
        )
