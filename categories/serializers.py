from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        # fields, exclude 둘 중에 하나만 사용
        # 보여줄 때 보여주고 싶은것
        # fields = (
        #     "name",
        #     "kind",
        # )
        # 보여줄 때 제외하고 싶은것
        # exclude = ("created_at",)
        # 모두 보여주고 싶을때
        fields = "__all__"


# class CategorySerializer(serializers.Serializer):
#     # 어떻게 출력이 될지를 정할 수 있다.
#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(
#         required=True,
#         max_length=50,
#     )
#     kind = serializers.ChoiceField(
#         # max_length=15,
#         choices=Category.CategoryKindChoices.choices,
#     )
#     created_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         # **validated_data는
#         # {"name": 'fdsa', "kind": "dfasf"}
#         # 이런 값을 name='fdsa', kind='dfasf' 이 형식으로 고쳐준다
#         return Category.objects.create(**validated_data)

#     # update가 되는 상황을 자동으로 인식해 update함수를 실행시켜준다.
#     # category 객체가 오지 않고 딕셔너리가 온 경우는 create
#     # category 객체가 오고 딕셔너리가 같이 오는 경우 update를 실행시켜준다
#     def update(self, instance, validated_data):
#         # if validated_data["name"]:
#         #     instance.name = validated_data["name"]

#         instance.name = validated_data.get("name", instance.name)
#         instance.kind = validated_data.get("kind", instance.kind)
#         instance.save()
#         return instance
