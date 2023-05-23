from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string

from .serializers import UserAuthSerializer

User = get_user_model()


class UserAuthView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserAuthSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if User.objects.filter(**request.data).exists:
            send_mail(
                'confirmation_code',
                get_random_string(length=16),
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )
