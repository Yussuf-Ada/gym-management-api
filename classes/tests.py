from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import GymClass, ClassBooking
from members.models import Member

User = get_user_model()


class GymClassTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.gym_class_data = {
            'name': 'Yoga Class',
            'description': 'Relaxing yoga session',
            'instructor': 'John Doe',
            'capacity': 20,
            'duration_minutes': 60,
            'schedule_day': 'monday',
            'schedule_time': '10:00:00'
        }

    def test_create_gym_class(self):
        url = reverse('gymclass-list')
        response = self.client.post(url, self.gym_class_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Yoga Class')
        self.assertEqual(GymClass.objects.count(), 1)

    def test_list_gym_classes(self):
        GymClass.objects.create(**self.gym_class_data)
        url = reverse('gymclass-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_gym_class_detail(self):
        gym_class = GymClass.objects.create(**self.gym_class_data)
        url = reverse('gymclass-detail', kwargs={'pk': gym_class.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['capacity'], 20)

    def test_update_gym_class(self):
        gym_class = GymClass.objects.create(**self.gym_class_data)
        url = reverse('gymclass-detail', kwargs={'pk': gym_class.pk})
        response = self.client.patch(url, {'capacity': 25})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['capacity'], 25)

    def test_delete_gym_class(self):
        gym_class = GymClass.objects.create(**self.gym_class_data)
        url = reverse('gymclass-detail', kwargs={'pk': gym_class.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GymClass.objects.count(), 0)


class ClassBookingTests(APITestCase):
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
        self.gym_class = GymClass.objects.create(
            name='Yoga Class',
            capacity=2,
            schedule_day='tuesday',
            schedule_time='14:00:00',
            instructor='John Doe',
            duration_minutes=60
        )

    def test_book_class(self):
        url = reverse('booking-list')
        response = self.client.post(url, {
            'member': self.member.pk,
            'gym_class': self.gym_class.pk,
            'booking_date': timezone.now().date()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClassBooking.objects.count(), 1)
        self.assertEqual(self.gym_class.current_bookings(), 1)

    def test_list_bookings(self):
        ClassBooking.objects.create(
            member=self.member,
            gym_class=self.gym_class,
            booking_date=timezone.now().date()
        )
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_capacity_validation(self):
        # Fill the class to capacity
        member2 = Member.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='0987654321'
        )
        
        ClassBooking.objects.create(member=self.member, gym_class=self.gym_class)
        ClassBooking.objects.create(member=member2, gym_class=self.gym_class)
        
        # Try to book when full
        member3 = Member.objects.create(
            first_name='Bob',
            last_name='Jones',
            email='bob@example.com',
            phone='1122334455'
        )
        
        url = reverse('booking-list')
        response = self.client.post(url, {
            'member': member3.pk,
            'gym_class': self.gym_class.pk
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Class is full', str(response.data))

    def test_cancel_booking(self):
        booking = ClassBooking.objects.create(
            member=self.member,
            gym_class=self.gym_class
        )
        url = reverse('booking-detail', kwargs={'pk': booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ClassBooking.objects.count(), 0)

    def test_filter_by_status(self):
        ClassBooking.objects.create(
            member=self.member,
            gym_class=self.gym_class,
            status='confirmed'
        )
        url = reverse('booking-list') + '?status=confirmed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
