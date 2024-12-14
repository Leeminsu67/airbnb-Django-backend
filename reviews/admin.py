from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            # 튜플 타입의 두번째 인자는 UI에 보이는 것
            # 첫번째 인자는 실제 필터를 검색하는 value
            (
                "good",
                "Good",
            ),
            (
                "great",
                "Great",
            ),
            (
                "awesome",
                "Awesome",
            ),
        ]

    # queryset은 필터링된 객체 즉, 필터링된 review를 리턴해야하는 메소드
    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


# 좋은 리뷰 나쁜 리뷰를 필터링 하는 필터 만들기
# 3점이상은 좋은 리뷰 3점 미만은 나쁜 리뷰
class CustomRatingFilter(admin.SimpleListFilter):
    title = "Custom Rating Filter"
    parameter_name = "custom_rating"

    def lookups(self, request, model_admin):
        return [
            (
                "good",
                "good reviews",
            ),
            (
                "bad",
                "bad reviews",
            ),
        ]

    def queryset(self, request, reviews):
        reviewFilter = self.value()

        if reviewFilter:
            return (
                # 이상
                reviews.filter(rating__gte=3)
                if reviewFilter == "good"
                # 미만
                else reviews.filter(rating__lt=3)
            )
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        CustomRatingFilter,
        "rating",
        # FK가 된 클래스에 있는 컬럼으로 filter가능
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
