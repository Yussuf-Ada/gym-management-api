from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'date_of_birth', 'emergency_contact', 'is_active', 'joined_date',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'joined_date', 'created_at', 'updated_at')


class MemberListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = ('id', 'full_name', 'email', 'phone', 'is_active', 'joined_date')
