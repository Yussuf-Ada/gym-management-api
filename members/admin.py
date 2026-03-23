from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_active', 'joined_date')
    list_filter = ('is_active', 'joined_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
