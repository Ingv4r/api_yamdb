from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
