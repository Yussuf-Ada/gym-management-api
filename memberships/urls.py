from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembershipViewSet, MemberMembershipViewSet

router = DefaultRouter()
router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'subscriptions', MemberMembershipViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]
