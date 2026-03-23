import uuid
from django.db import models
from django.core.exceptions import ValidationError


class GymClass(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    schedule_day = models.CharField(max_length=10, choices=DAY_CHOICES)
    schedule_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['schedule_day', 'schedule_time']
        verbose_name_plural = 'Gym Classes'

    def __str__(self):
        return f"{self.name} - {self.schedule_day} {self.schedule_time}"

    @property
    def spots_available(self):
        return self.capacity - self.bookings.filter(status='confirmed').count()


class ClassBooking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='bookings')
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='class_bookings')
    booking_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date', '-created_at']
        unique_together = ['gym_class', 'member', 'booking_date']

    def __str__(self):
        return f"{self.member} - {self.gym_class.name} ({self.booking_date})"

    def clean(self):
        if self.status == 'confirmed':
            confirmed_count = ClassBooking.objects.filter(
                gym_class=self.gym_class,
                booking_date=self.booking_date,
                status='confirmed'
            ).exclude(pk=self.pk).count()
            if confirmed_count >= self.gym_class.capacity:
                raise ValidationError('Class is fully booked')
