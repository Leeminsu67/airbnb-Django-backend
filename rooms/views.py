from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomSerializer, RoomDetailSerializer


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

        # return Response(
        #     AmenitySerializer(
        #         self.get_object(pk),
        #     ).data,
        # )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, requeest):
        # serializer에게 owner는 이 URL을 호출한 사람이 될거라고 말해주고 싶음
        # 하지만 먼저 유저가 인증되었는지 확인
        # request를 보내는 유저가 로그인 중인지 아닌지 체크
        if requeest.user.is_authenticated:
            serializer = RoomDetailSerializer(data=requeest.data)
            if serializer.is_valid():
                # Category
                category_pk = requeest.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

                room = serializer.save(
                    owner=requeest.user,
                    category=category,
                )
                # Amenity
                amenities = requeest.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    except Amenity.DoesNotExist:
                        raise ParseError(f"Amenity with id {amenity_pk} not found")

                return Response(RoomDetailSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


"""
{
    "name": "House created with DRF",
    "country": "한국",
    "city": "서울",
    "price": 1000,
    "rooms": 2,
    "toilets": 2,
    "description": "DRF is great!",
    "address": "123",
    "pet_friendly": true,
    "kind": "private_room",
    "category": 1,
    "amenities": [1,2,3,4]
}
"""


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
