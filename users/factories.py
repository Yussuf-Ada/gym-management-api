import factory
from django.contrib.auth import get_user_model
from members.factories import MembershipFactory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or factory.Faker('password')
        self.set_password(password)
        self.save()


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class MemberUserFactory(UserFactory):
    @factory.post_generation
    def memberships(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for membership in extracted:
                self.memberships.add(membership)
        else:
            # Create a default membership
            membership = MembershipFactory()
            self.memberships.add(membership)
