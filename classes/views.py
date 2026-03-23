from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GymClass, ClassBooking
from .serializers import GymClassSerializer, ClassBookingSerializer


class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('schedule_day', 'is_active', 'instructor')
    search_fields = ('name', 'instructor', 'description')
    ordering_fields = ('name', 'schedule_day', 'schedule_time', 'capacity')
    ordering = ('schedule_day', 'schedule_time')


class ClassBookingViewSet(viewsets.ModelViewSet):
    queryset = ClassBooking.objects.select_related('gym_class', 'member').all()
    serializer_class = ClassBookingSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('gym_class', 'member', 'status', 'booking_date')
    ordering_fields = ('booking_date', 'created_at')
    ordering = ('-booking_date',)
