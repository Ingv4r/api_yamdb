from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions


User = get_user_model()


class MyTokenObtainSerializer(serializers.ModelSerializer):
    token_class = SlidingToken

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        if data.get('confirmation_code') == user.confirmation_code:
            token = self.get_token(user)
            user.confirmation_code = None
            print(user.confirmation_code)
            return {'token': str(token)}
        raise exceptions.ValidationError(
            'Invalid confirmation_code'
        )

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
