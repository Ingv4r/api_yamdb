from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class MyTokenObtainSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""
    token_class = AccessToken

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate(self, data):
        """Проверка валидности confirmation_code."""
        user = get_object_or_404(User, username=data.get("username"))
        if data.get("confirmation_code") == str(user.activation_code):
            token = self.get_token(user)
            return {"token": str(token)}
        raise exceptions.ValidationError("Invalid confirmation_code")

    @classmethod
    def get_token(cls, user):
        """Получить AccessToken."""
        return cls.token_class.for_user(user)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("title",)

    def validate(self, data):
        if self.context["request"].method == "POST":
            if Review.objects.filter(
                author=self.context["request"].user,
                title=self.context["view"].kwargs.get("title_id"),
            ).exists():
                raise serializers.ValidationError(
                    "Нельзя оставить отзыв на одно произведение дважды"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("review", "author")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        exclude = ("id",)
        model = Genre
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных произведений."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = ("genre", "rating")


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи данных произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class AuthSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации."""
    username = serializers.RegexField(r"^[\w.@+-]+\Z", max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        """Проверка уже зарегестрированных пользователей."""
        email_exists = User.objects.filter(email=data.get("email")).exists()
        username_exists = User.objects.filter(
            username=data.get("username")
        ).exists()
        if data.get("username") == "me":
            raise serializers.ValidationError("Username cannot be 'me'")
        if email_exists and not username_exists:
            raise serializers.ValidationError(
                "A user with this email already exists!"
            )
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                "A user with this username already exists!"
            )
        return data


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователей админом."""
    username = serializers.RegexField(r"^[\w.@+-]+\Z", max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_email(self, value):
        """Проверка сущестования пользователя с данным email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists!"
            )
        return value

    def validate_username(self, value):
        """Проверка существования пользователя по username."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists!"
            )
        return value


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и редкатирования информации пользователем."""
    username = serializers.RegexField(r"^[\w.@+-]+\Z", max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
