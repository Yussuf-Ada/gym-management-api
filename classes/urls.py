from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymClassViewSet, ClassBookingViewSet

router = DefaultRouter()
router.register(r'classes', GymClassViewSet, basename='gymclass')
router.register(r'bookings', ClassBookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
