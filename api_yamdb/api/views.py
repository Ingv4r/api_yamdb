from rest_framework_simplejwt.views import TokenObtainSlidingView
from .serializers import MyTokenObtainSerializer


class MyTokenObtainSlidingView(TokenObtainSlidingView):

    serializer_class = MyTokenObtainSerializer
