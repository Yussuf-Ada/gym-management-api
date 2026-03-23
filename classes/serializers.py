from rest_framework import serializers
from .models import GymClass


class GymClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymClass
        fields = (
            'id', 'name', 'description', 'instructor', 'capacity',
            'duration_minutes', 'schedule_day', 'schedule_time',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
