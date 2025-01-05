from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    # post를 할 때 유저를 묻지 않을거기 때문에 read_only를 붙여준다
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
