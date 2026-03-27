from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PasswordResetToken
from members.models import Member
from memberships.models import Membership, MemberMembership

User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'WrongPass123!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('user_profile')

    def test_get_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile(self):
        response = self.client.patch(self.profile_url, {'first_name': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')


class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!',
            role='admin'
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

    def test_dashboard_stats(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_members', response.data)
        self.assertIn('active_subscriptions', response.data)
        self.assertEqual(response.data['total_members'], 1)


class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!'
        )
        self.reset_request_url = reverse('password_reset_request')
        self.reset_confirm_url = reverse('password_reset_confirm')

    def test_password_reset_request(self):
        response = self.client.post(self.reset_request_url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PasswordResetToken.objects.count(), 1)

    def test_password_reset_invalid_email(self):
        response = self.client.post(self.reset_request_url, {'email': 'wrong@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Returns 200 for security
        self.assertEqual(PasswordResetToken.objects.count(), 0)  # No token created

    def test_password_reset_confirm(self):
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='test-token-123',
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )
        response = self.client.post(self.reset_confirm_url, {
            'token': token.token,
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token.refresh_from_db()
        self.assertTrue(token.used)

    def test_password_reset_expired_token(self):
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='expired-token',
            expires_at=timezone.now() - timezone.timedelta(hours=1)
        )
        response = self.client.post(self.reset_confirm_url, {
            'token': token.token,
            'new_password': 'NewPass123!'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
