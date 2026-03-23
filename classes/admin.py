from django.contrib import admin
from .models import GymClass


@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'schedule_day', 'schedule_time', 'capacity', 'is_active')
    list_filter = ('schedule_day', 'is_active', 'instructor')
    search_fields = ('name', 'instructor')
