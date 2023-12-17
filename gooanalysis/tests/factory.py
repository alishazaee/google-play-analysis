from django.contrib.auth import get_user_model
import factory
from faker import Faker
from django.utils import timezone
from gooanalysis.applists.models import Applications
faker = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Applications
    
    app_id = factory.LazyAttribute(lambda _ :f'{faker.unique.app_id()}')
    category = factory.LazyAttribute(lambda _: 0 )
    name = factory.LazyAttribute(lambda _: 0 )
