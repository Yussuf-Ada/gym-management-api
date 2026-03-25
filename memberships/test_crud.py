from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Membership, MemberMembership
from members.models import Member

User = get_user_model()


class MembershipCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.membership_data = {
            'name': 'Premium Plan',
            'description': 'Premium gym membership',
            'price': '99.99',
            'duration_days': 30
        }

    def test_create_membership(self):
        """Test creating a new membership"""
        url = reverse('membership-list')
        response = self.client.post(url, self.membership_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Membership.objects.count(), 1)
        self.assertEqual(response.data['name'], 'Premium Plan')

    def test_list_memberships(self):
        """Test listing all memberships"""
        url = reverse('membership-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_update_membership(self):
        """Test updating a membership"""
        membership = Membership.objects.create(**self.membership_data)
        url = reverse('membership-detail', kwargs={'pk': membership.pk})
        response = self.client.patch(url, {'price': '149.99'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '149.99')

    def test_delete_membership(self):
        """Test deleting a membership"""
        membership = Membership.objects.create(**self.membership_data)
        url = reverse('membership-detail', kwargs={'pk': membership.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Membership.objects.count(), 0)
