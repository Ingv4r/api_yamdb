from rest_framework_simplejwt.views import TokenObtainSlidingView

from .serializers import MyTokenObtainSerializer


class MyTokenObtainSlidingView(TokenObtainSlidingView):
    '''Docsting'''
    serializer_class = MyTokenObtainSerializer
