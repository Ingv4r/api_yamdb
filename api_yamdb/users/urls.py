from django.urls import include, path
from rest_framework import routers

from .views import UserAuthView


app_name = 'users'
router = routers.DefaultRouter()
router.register('auth/signup', UserAuthView)

urlpatterns = [
    path('v1/', include(router.urls)),
]
