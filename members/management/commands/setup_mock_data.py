from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from members.models import Member
from memberships.models import Membership, MemberMembership
from classes.models import GymClass, ClassBooking
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Drop all data and create mock data for demo purposes'

    def handle(self, *args, **options):
        self.stdout.write('Dropping all existing data...')
        
        # Drop all data
        ClassBooking.objects.all().delete()
        MemberMembership.objects.all().delete()
        GymClass.objects.all().delete()
        Membership.objects.all().delete()
        Member.objects.all().delete()
        User.objects.all().delete()
        
        self.stdout.write('Creating mock data...')
        
        # Create admin user
        admin = User.objects.create_user(
            email='admin@gym.com',
            first_name='Admin',
            last_name='User',
            password='admin123'
        )
        
        # Create mock members
        members_data = [
            {'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@email.com', 'phone': '07700900001', 'date_of_birth': '1990-05-15'},
            {'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.j@email.com', 'phone': '07700900002', 'date_of_birth': '1985-08-22'},
            {'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike.w@email.com', 'phone': '07700900003', 'date_of_birth': '1992-03-10'},
            {'first_name': 'Emma', 'last_name': 'Davis', 'email': 'emma.d@email.com', 'phone': '07700900004', 'date_of_birth': '1988-12-05'},
            {'first_name': 'James', 'last_name': 'Brown', 'email': 'james.b@email.com', 'phone': '07700900005', 'date_of_birth': '1995-07-18'},
            {'first_name': 'Lisa', 'last_name': 'Anderson', 'email': 'lisa.a@email.com', 'phone': '07700900006', 'date_of_birth': '1991-09-30'},
            {'first_name': 'David', 'last_name': 'Miller', 'email': 'david.m@email.com', 'phone': '07700900007', 'date_of_birth': '1987-04-12'},
            {'first_name': 'Rachel', 'last_name': 'Taylor', 'email': 'rachel.t@email.com', 'phone': '07700900008', 'date_of_birth': '1993-11-25'},
            {'first_name': 'Tom', 'last_name': 'Moore', 'email': 'tom.m@email.com', 'phone': '07700900009', 'date_of_birth': '1989-06-08'},
            {'first_name': 'Amy', 'last_name': 'White', 'email': 'amy.w@email.com', 'phone': '07700900010', 'date_of_birth': '1994-02-14'},
        ]
        
        members = []
        for member_data in members_data:
            member = Member.objects.create(
                joined_date=date.today() - timedelta(days=30),
                is_active=True,
                **member_data
            )
            members.append(member)
        
        # Create membership plans
        memberships_data = [
            {'name': 'Basic', 'description': 'Access to gym equipment during opening hours', 'price': 29.99, 'duration_days': 30},
            {'name': 'Premium', 'description': 'Basic + access to all group classes', 'price': 49.99, 'duration_days': 30},
            {'name': 'VIP', 'description': 'Premium + personal trainer sessions', 'price': 89.99, 'duration_days': 30},
            {'name': 'Student', 'description': 'Discounted rate for students', 'price': 19.99, 'duration_days': 30},
            {'name': 'Annual', 'description': 'Best value - 12 months membership', 'price': 499.99, 'duration_days': 365},
        ]
        
        memberships = []
        for membership_data in memberships_data:
            membership = Membership.objects.create(**membership_data)
            memberships.append(membership)
        
        # Create member subscriptions
        subscriptions_data = [
            {'member': members[0], 'membership': memberships[1], 'start_date': date.today() - timedelta(days=15)}, # John - Premium
            {'member': members[1], 'membership': memberships[0], 'start_date': date.today() - timedelta(days=10)}, # Sarah - Basic
            {'member': members[2], 'membership': memberships[2], 'start_date': date.today() - timedelta(days=5)},  # Mike - VIP
            {'member': members[3], 'membership': memberships[1], 'start_date': date.today() - timedelta(days=20)}, # Emma - Premium
            {'member': members[4], 'membership': memberships[3], 'start_date': date.today() - timedelta(days=8)},  # James - Student
            {'member': members[5], 'membership': memberships[2], 'start_date': date.today() - timedelta(days=12)}, # Lisa - VIP
            {'member': members[6], 'membership': memberships[0], 'start_date': date.today() - timedelta(days=25)}, # David - Basic
            {'member': members[7], 'membership': memberships[4], 'start_date': date.today() - timedelta(days=30)}, # Rachel - Annual
        ]
        
        for sub_data in subscriptions_data:
            MemberMembership.objects.create(**sub_data)
        
        # Create gym classes
        classes_data = [
            {'name': 'Morning Yoga', 'instructor': 'Sarah Chen', 'schedule_day': 'monday', 'schedule_time': '07:00:00', 'duration_minutes': 60, 'capacity': 15},
            {'name': 'HIIT Training', 'instructor': 'Mike Johnson', 'schedule_day': 'monday', 'schedule_time': '18:00:00', 'duration_minutes': 45, 'capacity': 20},
            {'name': 'Pilates', 'instructor': 'Emma Wilson', 'schedule_day': 'tuesday', 'schedule_time': '09:00:00', 'duration_minutes': 50, 'capacity': 12},
            {'name': 'Spin Class', 'instructor': 'Tom Davis', 'schedule_day': 'tuesday', 'schedule_time': '17:30:00', 'duration_minutes': 45, 'capacity': 25},
            {'name': 'Boxing Fitness', 'instructor': 'James Miller', 'schedule_day': 'wednesday', 'schedule_time': '19:00:00', 'duration_minutes': 60, 'capacity': 18},
            {'name': 'Zumba', 'instructor': 'Lisa Anderson', 'schedule_day': 'thursday', 'schedule_time': '18:30:00', 'duration_minutes': 55, 'capacity': 30},
            {'name': 'Strength Training', 'instructor': 'David Brown', 'schedule_day': 'friday', 'schedule_time': '07:30:00', 'duration_minutes': 60, 'capacity': 15},
            {'name': 'Aqua Aerobics', 'instructor': 'Rachel Taylor', 'schedule_day': 'saturday', 'schedule_time': '10:00:00', 'duration_minutes': 45, 'capacity': 20},
            {'name': 'Evening Yoga', 'instructor': 'Sarah Chen', 'schedule_day': 'saturday', 'schedule_time': '16:00:00', 'duration_minutes': 60, 'capacity': 15},
            {'name': 'Sunday Circuit', 'instructor': 'Mike Johnson', 'schedule_day': 'sunday', 'schedule_time': '11:00:00', 'duration_minutes': 60, 'capacity': 25},
        ]
        
        gym_classes = []
        for class_data in classes_data:
            gym_class = GymClass.objects.create(**class_data)
            gym_classes.append(gym_class)
        
        # Create class bookings
        bookings_data = [
            {'member': members[0], 'gym_class': gym_classes[0], 'booking_date': date.today() + timedelta(days=1)}, # John - Morning Yoga
            {'member': members[1], 'gym_class': gym_classes[1], 'booking_date': date.today() + timedelta(days=1)}, # Sarah - HIIT
            {'member': members[2], 'gym_class': gym_classes[2], 'booking_date': date.today() + timedelta(days=2)}, # Mike - Pilates
            {'member': members[3], 'gym_class': gym_classes[3], 'booking_date': date.today() + timedelta(days=2)}, # Emma - Spin
            {'member': members[4], 'gym_class': gym_classes[4], 'booking_date': date.today() + timedelta(days=3)}, # James - Boxing
            {'member': members[5], 'gym_class': gym_classes[5], 'booking_date': date.today() + timedelta(days=3)}, # Lisa - Zumba
            {'member': members[6], 'gym_class': gym_classes[6], 'booking_date': date.today() + timedelta(days=4)}, # David - Strength
            {'member': members[7], 'gym_class': gym_classes[7], 'booking_date': date.today() + timedelta(days=5)}, # Rachel - Aqua
            {'member': members[8], 'gym_class': gym_classes[8], 'booking_date': date.today() + timedelta(days=5)}, # Tom - Evening Yoga
            {'member': members[9], 'gym_class': gym_classes[9], 'booking_date': date.today() + timedelta(days=6)}, # Amy - Sunday Circuit
        ]
        
        for booking_data in bookings_data:
            ClassBooking.objects.create(**booking_data)
        
        self.stdout.write(self.style.SUCCESS('Mock data created successfully!'))
        self.stdout.write(f'Created {len(members)} members')
        self.stdout.write(f'Created {len(memberships)} membership plans')
        self.stdout.write(f'Created {len(subscriptions_data)} subscriptions')
        self.stdout.write(f'Created {len(gym_classes)} gym classes')
        self.stdout.write(f'Created {len(bookings_data)} class bookings')
        self.stdout.write('Admin user: admin@gym.com / admin123')
