from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymClassViewSet

router = DefaultRouter()
router.register(r'classes', GymClassViewSet, basename='gymclass')

urlpatterns = [
    path('', include(router.urls)),
]
