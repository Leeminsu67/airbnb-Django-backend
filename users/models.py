from django.db import models
from django.contrib.auth.models import AbstractUser


# Django의 User부분을 모두 사용하지만 더욱 확장해 나갈 수 있다.
# 커스텀 모델 클래스
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        # 튜플의 처음 인자는 데이터베이스에 들어갈 value를 갖고 있고
        # 두번째 인자는 관리자 페이지에서 보게되는 label을 가지고 있다
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # avatar = models.ImageField()
    # blank=True는 필드가 필수적이지 않게 해준다(null 허용처럼)
    avatar = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    # default값 부여
    # null 허용
    # 두가지 중에 하나를 하면 해결할 수 있음
    # is_host = models.BooleanField(null=True)
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
