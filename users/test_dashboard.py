from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from members.models import Member
from memberships.models import Membership, MemberMembership

User = get_user_model()


class DashboardAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.dashboard_url = reverse('dashboard_stats')
        
        # Create test data
        self.member = Member.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890'
        )
        
        self.membership = Membership.objects.create(
            name='Basic Plan',
            price='29.99',
            duration_days=30
        )
        
        MemberMembership.objects.create(
            member=self.member,
            membership=self.membership,
            start_date=timezone.now()
        )

    def test_dashboard_stats_endpoint(self):
        """Test dashboard statistics API endpoint"""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check required fields
        self.assertIn('total_members', response.data)
        self.assertIn('active_subscriptions', response.data)
        self.assertIn('expiring_soon', response.data)
        
        # Check data accuracy
        self.assertEqual(response.data['total_members'], 1)
        self.assertEqual(response.data['active_subscriptions'], 1)

    def test_dashboard_unauthorized(self):
        """Test dashboard endpoint requires authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
