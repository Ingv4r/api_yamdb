from reviews.models import (
    Comment, Genre, Category, Title, Review
)

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class MyTokenObtainSerializer(serializers.ModelSerializer):
    '''Docsting'''
    token_class = AccessToken

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        '''Docsting'''
        user = get_object_or_404(User, username=data.get('username'))
        if data.get('confirmation_code') == str(user.activation_code):
            token = self.get_token(user)
            return {'token': str(token)}
        raise exceptions.ValidationError(
            'Invalid confirmation_code'
        )

    @classmethod
    def get_token(cls, user):
        '''Docsting'''
        return cls.token_class.for_user(user)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['view'].kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'author')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных произведений."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genre', 'rating')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи данных произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class AuthSerializer(serializers.ModelSerializer):
    '''Docsting'''
    username = serializers.RegexField(r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        '''Docsting'''
        email_exists = User.objects.filter(email=data.get('email')).exists()
        username_exists = User.objects.filter(
            username=data.get('username')
        ).exists()
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                "Username cannot be 'me'"
            )
        if email_exists and not username_exists:
            raise serializers.ValidationError(
                'A user with this email already exists!'
            )
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                'A user with this username already exists!'
            )
        return data


class AdminSerializer(serializers.ModelSerializer):
    '''Docsting'''
    username = serializers.RegexField(r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_email(self, value):
        '''Docsting'''
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists!"
            )
        return value

    def validate_username(self, value):
        '''Docsting'''
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'A user with this username already exists!'
            )
        return value


class MeSerializer(serializers.ModelSerializer):
    '''Docsting'''
    username = serializers.RegexField(r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
