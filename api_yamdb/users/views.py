from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string


from .serializers import UserAuthSerializer

User = get_user_model()


class UserAuthView(viewsets.ViewSet):
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            confirmation_code = get_random_string(length=16)
            serializer.save(confirmation_code=confirmation_code)
            send_mail(
                'confirmation_code',
                confirmation_code,
                'from@example.com',
                [request.data.get('email')],
                fail_silently=False,
            )
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
