from django.conf import settings
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer


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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        # serializer에게 owner는 이 URL을 호출한 사람이 될거라고 말해주고 싶음
        # 하지만 먼저 유저가 인증되었는지 확인
        # request를 보내는 유저가 로그인 중인지 아닌지 체크
        # if request.user.is_authenticated:
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Category
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            # 트랜잭션
            try:
                # transaction을 사용하기 때문에 애초에 방이 생성되질 않는다
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    # Amenity
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
            except Exception:
                raise ParseError("Amenity not found")
            return Response(RoomDetailSerializer(room).data)
        else:
            return Response(serializer.errors)

    # else:
    #     raise NotAuthenticated


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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            # Category
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError(detail="The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError(detail="Category not found")

            # 트랜잭션 실행
            try:
                with transaction.atomic():
                    # Category check
                    if category_pk:
                        updated_room = serializer.save(category=category)
                    else:
                        updated_room = serializer.save()

                    # Amenity
                    amenities = request.data.get("amenities")
                    if amenities:
                        updated_room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)
                    else:
                        updated_room.amenities.clear()

                return Response(RoomDetailSerializer(updated_room).data)
            except Exception:
                raise ParseError(detail="Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # 숫자가 아닌 경우를 예외처리하기 위함
        try:
            # get함수에 기본값을 설정할 수 있음 두번째 인자에 넣어주면 된다
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        # pagenation 로직 구현
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            # 모든 데이터를 가지고 와서 배열별로 자르는게 아닌
            # start와 end가 offset과 LIMIT 쿼리로 변환이 되어 쿼리 속도가 빠르게 된다
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(
                room=room,
            )
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # 현재시간
        now = timezone.localtime(timezone.now()).date()
        # 년도와 월 정보를 query_params로 받아온다
        try:
            month = int(request.query_params.get("month", now.month))
            year = int(request.query_params.get("year", now.year))
            if year < now.year:
                year = now.year
                month = now.month
            elif (year == now.year) and (month < now.month):
                month = now.month

        except:
            month = now.month
            year = now.year

        search_date_start = now.replace(year=year, month=month, day=1)

        next_month = month + 1 if month < 12 else 1
        next_month_year = year if month < 12 else year + 1
        search_date_end = now.replace(year=next_month_year, month=next_month, day=1)

        # pagenation
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            # check_in 날짜가 (우리가 있는 곳의) 현재 날짜보다 큰 booking을 찾고 있음
            check_in__gt=search_date_start,
            check_in__lt=search_date_end,
        )
        serializer = PublicBookingSerializer(
            bookings.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
