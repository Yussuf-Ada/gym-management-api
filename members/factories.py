import factory
from factory import fuzzy
from django.utils import timezone
from .models import Member, Membership, GymClass, Booking


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership
    
    name = factory.Faker('word')
    description = factory.Faker('text')
    price = fuzzy.FuzzyDecimal(10.0, 200.0, 2)
    duration_months = fuzzy.FuzzyInteger(1, 12)
    features = factory.List([factory.Faker('word') for _ in range(3)])


class GymClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GymClass
    
    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    instructor = factory.Faker('name')
    schedule = factory.Faker('time')
    max_capacity = fuzzy.FuzzyInteger(5, 30)
    duration_minutes = fuzzy.FuzzyInteger(30, 120)


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member
    
    user = factory.SubFactory('users.factories.UserFactory')
    phone = factory.Faker('phone_number')
    emergency_contact = factory.Faker('name')
    emergency_phone = factory.Faker('phone_number')
    medical_notes = factory.Faker('text')
    join_date = factory.LazyFunction(timezone.now)
    
    @factory.post_generation
    def memberships(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for membership in extracted:
                self.memberships.add(membership)


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
    
    member = factory.SubFactory(MemberFactory)
    gym_class = factory.SubFactory(GymClassFactory)
    booking_date = factory.LazyFunction(timezone.now)
    status = fuzzy.FuzzyChoice(['confirmed', 'cancelled', 'completed'])
    notes = factory.Faker('text')
