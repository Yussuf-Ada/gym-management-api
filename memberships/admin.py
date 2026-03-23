from django.contrib import admin
from .models import Membership, MemberMembership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(MemberMembership)
class MemberMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'membership', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'membership')
    search_fields = ('member__first_name', 'member__last_name', 'member__email')
    raw_id_fields = ('member',)
