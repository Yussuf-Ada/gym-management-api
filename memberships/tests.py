from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Membership, MemberMembership
from members.models import Member

User = get_user_model()


class MembershipTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.membership_data = {
            'name': 'Basic Plan',
            'description': 'Basic gym membership',
            'price': '29.99',
            'duration_days': 30
        }

    def test_create_membership(self):
        url = reverse('membership-list')
        response = self.client.post(url, self.membership_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Basic Plan')
        self.assertEqual(Membership.objects.count(), 1)

    def test_list_memberships(self):
        Membership.objects.create(**self.membership_data)
        url = reverse('membership-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_membership_detail(self):
        membership = Membership.objects.create(**self.membership_data)
        url = reverse('membership-detail', kwargs={'pk': membership.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '29.99')

    def test_update_membership(self):
        membership = Membership.objects.create(**self.membership_data)
        url = reverse('membership-detail', kwargs={'pk': membership.pk})
        response = self.client.patch(url, {'price': '39.99'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '39.99')

    def test_delete_membership(self):
        membership = Membership.objects.create(**self.membership_data)
        url = reverse('membership-detail', kwargs={'pk': membership.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Membership.objects.count(), 0)


class MemberMembershipTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.client.force_authenticate(user=self.user)
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

    def test_subscribe_member(self):
        url = reverse('subscription-list')
        response = self.client.post(url, {
            'member': self.member.pk,
            'membership': self.membership.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MemberMembership.objects.count(), 1)

    def test_list_subscriptions(self):
        MemberMembership.objects.create(
            member=self.member,
            membership=self.membership,
            start_date=timezone.now().date()
        )
        url = reverse('subscription-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_active_subscriptions(self):
        MemberMembership.objects.create(
            member=self.member,
            membership=self.membership,
            start_date=timezone.now().date()
        )
        url = reverse('subscription-list') + '?is_active=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_expiry(self):
        expired_subscription = MemberMembership.objects.create(
            member=self.member,
            membership=self.membership,
            start_date=timezone.now().date() - timezone.timedelta(days=31)
        )
        self.assertTrue(expired_subscription.is_expired)
