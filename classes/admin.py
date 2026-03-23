from django.contrib import admin
from .models import GymClass, ClassBooking


@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'schedule_day', 'schedule_time', 'capacity', 'is_active')
    list_filter = ('schedule_day', 'is_active', 'instructor')
    search_fields = ('name', 'instructor')


@admin.register(ClassBooking)
class ClassBookingAdmin(admin.ModelAdmin):
    list_display = ('member', 'gym_class', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'gym_class')
    search_fields = ('member__first_name', 'member__last_name', 'gym_class__name')
    raw_id_fields = ('member', 'gym_class')
