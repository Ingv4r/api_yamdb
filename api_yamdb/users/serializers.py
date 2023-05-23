from rest_framework import exceptions, serializers, validators
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.CharField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    