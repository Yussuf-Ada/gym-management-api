import uuid
from django.db import models


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
