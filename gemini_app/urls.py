from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register('register', UserViewSet, basename="register"),
router.register('login', LoginViewSet, basename="login")

urlpatterns = []

urlpatterns += router.urls