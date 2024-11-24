from django.db import models


# 다른 model에서 재사용하기 위한 model
# 데이터베이스에는 생성되지 않는 class
class CommonModel(models.Model):
    """Common Model Definition"""

    # auto_now_add 필드의 값은 object가 처음 생성되었을 때 시간으로 설정됨
    created_at = models.DateTimeField(auto_now_add=True)
    # 처음 생성되거나 해당 row가 업데이트될 때 마다 시간이 설정된다
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Django가 model을 봐도 이걸 데이터베이스 저장하지 않을것임 abstract
        abstract = True
