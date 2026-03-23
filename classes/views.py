from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GymClass
from .serializers import GymClassSerializer


class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('schedule_day', 'is_active', 'instructor')
    search_fields = ('name', 'instructor', 'description')
    ordering_fields = ('name', 'schedule_day', 'schedule_time', 'capacity')
    ordering = ('schedule_day', 'schedule_time')
