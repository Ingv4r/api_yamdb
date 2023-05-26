from django.urls import path

from .views import MyTokenObtainSlidingView

app_name = 'api'

urlpatterns = [
    path(
        'v1/auth/token/',
        MyTokenObtainSlidingView.as_view(),
        name='token_obtain_view'
    ),
]
