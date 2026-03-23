from rest_framework import serializers
from datetime import date
from .models import Membership, MemberMembership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'name', 'description', 'price', 'duration_days', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class MemberMembershipSerializer(serializers.ModelSerializer):
    membership_name = serializers.CharField(source='membership.name', read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = MemberMembership
        fields = (
            'id', 'member', 'member_name', 'membership', 'membership_name',
            'start_date', 'end_date', 'status', 'is_expired', 'days_remaining',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'end_date', 'created_at', 'updated_at')

    def create(self, validated_data):
        if 'start_date' not in validated_data:
            validated_data['start_date'] = date.today()
        return super().create(validated_data)
