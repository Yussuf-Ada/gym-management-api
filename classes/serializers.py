from rest_framework import serializers
from .models import GymClass, ClassBooking


class GymClassSerializer(serializers.ModelSerializer):
    spots_available = serializers.ReadOnlyField()

    class Meta:
        model = GymClass
        fields = (
            'id', 'name', 'description', 'instructor', 'capacity', 'spots_available',
            'duration_minutes', 'schedule_day', 'schedule_time',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ClassBookingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='gym_class.name', read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)

    class Meta:
        model = ClassBooking
        fields = (
            'id', 'gym_class', 'class_name', 'member', 'member_name',
            'booking_date', 'status', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        gym_class = attrs.get('gym_class') or self.instance.gym_class
        booking_date = attrs.get('booking_date') or self.instance.booking_date
        status = attrs.get('status', 'confirmed')

        if status == 'confirmed':
            confirmed_count = ClassBooking.objects.filter(
                gym_class=gym_class,
                booking_date=booking_date,
                status='confirmed'
            ).exclude(pk=getattr(self.instance, 'pk', None)).count()
            if confirmed_count >= gym_class.capacity:
                raise serializers.ValidationError({'gym_class': 'Class is fully booked'})
        return attrs
