from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'date_of_birth', 'emergency_contact', 'profile_image', 'profile_image_url', 'is_active', 'joined_date',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'joined_date', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        
        # Update other fields - only update if provided
        for attr, value in validated_data.items():
            if value is not None and value != '':
                setattr(instance, attr, value)
        
        # Handle image update
        if profile_image:
            print(f"Updating profile image: {profile_image}")
            instance.profile_image = profile_image
            print(f"Image URL after update: {instance.profile_image.url}")
        
        instance.save()
        return instance
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None


class MemberListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('id', 'full_name', 'email', 'phone', 'date_of_birth', 'emergency_contact', 'profile_image_url', 'is_active', 'joined_date')
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None
