from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ConfirmationCode
from .pagination import UsersPagination
from .permissions import SuperUserOrAdminOnly
from .serializers import AdminSerializer, AuthSerializer, MeSerializer

User = get_user_model()


class UserAuthView(viewsets.ViewSet):
    '''Docsting'''
    queryset = User.objects.all()

    def create(self, request):
        '''Docsting'''
        serializer = AuthSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = User.objects.get_or_create(
            username=username,
            email=email,
        )[0]
        code = ConfirmationCode.objects.get_or_create(user=user)[0]
        send_mail(
            'confirmation_code',
            str(code),
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    '''Docsting'''
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = UsersPagination
    permission_classes = (SuperUserOrAdminOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_object(self):
        '''Docsting'''
        username = self.kwargs[self.lookup_field]
        obj = get_object_or_404(User, username=username)
        return obj

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        '''Docsting'''
        user = get_object_or_404(User, pk=request.user.id)
        serializer = MeSerializer()
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':

            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
