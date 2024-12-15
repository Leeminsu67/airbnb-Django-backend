from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    # 어떻게 출력이 될지를 정할 수 있다.
    pk = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()
