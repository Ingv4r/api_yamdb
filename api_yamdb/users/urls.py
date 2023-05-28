from django.urls import include, path
from rest_framework import routers

from .views import UserAuthView, UsersViewSet

app_name = 'users'
router = routers.DefaultRouter()
router.register('auth/signup', UserAuthView)
router.register(r'users', UsersViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
