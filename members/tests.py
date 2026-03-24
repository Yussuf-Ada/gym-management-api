from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()


class MemberTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.member_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }

    def test_create_member(self):
        url = reverse('member-list')
        response = self.client.post(url, self.member_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(Member.objects.count(), 1)

    def test_list_members(self):
        Member.objects.create(**self.member_data)
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_detail(self):
        member = Member.objects.create(**self.member_data)
        url = reverse('member-detail', kwargs={'pk': member.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_update_member(self):
        member = Member.objects.create(**self.member_data)
        url = reverse('member-detail', kwargs={'pk': member.pk})
        response = self.client.patch(url, {'first_name': 'Jane'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')

    def test_delete_member(self):
        member = Member.objects.create(**self.member_data)
        url = reverse('member-detail', kwargs={'pk': member.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Member.objects.count(), 0)

    def test_search_members(self):
        Member.objects.create(**self.member_data)
        url = reverse('member-list') + '?search=John'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_active_members(self):
        Member.objects.create(**self.member_data)
        url = reverse('member-list') + '?is_active=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
