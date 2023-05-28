from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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
