from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    MyTokenObtainSlidingView,
    ReviewViewSet,
    TitleViewSet,
    UserAuthView,
    UsersViewSet,
)

app_name = "api"

router1 = DefaultRouter()
router1.register("auth/signup", UserAuthView)
router1.register(r"users", UsersViewSet)
router1.register("genres", GenreViewSet, basename="genres")
router1.register("categories", CategoryViewSet, basename="categories")
router1.register("titles", TitleViewSet, basename="titles")
router1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>[\d]+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path(
        "v1/auth/token/",
        MyTokenObtainSlidingView.as_view(),
        name="token_obtain_view",
    ),
    path("v1/", include(router1.urls)),
]
