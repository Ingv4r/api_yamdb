from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView
from reviews.models import Category, Genre, Review, Title
from users.models import ConfirmationCode

from .filtersets import TitleFilterSet
from .mixins import ModelMixinSet
from .permissions import (
    AuthorOrStuffOnly,
    IsAdminUserOrReadOnly,
    SuperUserOrAdminOnly,
)
from .serializers import (
    AdminSerializer,
    AuthSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MeSerializer,
    MyTokenObtainSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)

User = get_user_model()


class UserAuthView(viewsets.ViewSet):
    """Docsting"""

    queryset = User.objects.all()

    def create(self, request):
        """Docsting"""
        serializer = AuthSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        user = User.objects.get_or_create(
            username=username,
            email=email,
        )[0]
        code = ConfirmationCode.objects.get_or_create(user=user)[0]
        send_mail(
            "confirmation_code",
            str(code),
            "from@example.com",
            [user.email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Docsting"""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination
    permission_classes = (SuperUserOrAdminOnly,)
    http_method_names = ("get", "post", "patch", "delete")

    def get_object(self):
        """Docsting"""
        username = self.kwargs[self.lookup_field]
        obj = get_object_or_404(User, username=username)
        return obj

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Docsting"""
        user = get_object_or_404(User, pk=request.user.id)
        serializer = MeSerializer()
        if request.method == "GET":
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":

            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class MyTokenObtainSlidingView(TokenObtainSlidingView):
    """Docsting"""

    serializer_class = MyTokenObtainSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrStuffOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrStuffOnly)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(ModelMixinSet):
    """Получить список всех жанров без токена."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(ModelMixinSet):
    """Получить список всех категорий без токена."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет с произведениями."""

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = TitleFilterSet
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    search_fields = (
        "category__slug",
        "genre__slug",
        "name",
        "yaer",
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleReadSerializer
        return TitleWriteSerializer
