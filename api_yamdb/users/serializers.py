from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists!"
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists!"
            )
        return value
