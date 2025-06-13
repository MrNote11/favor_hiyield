from django.core.management.base import BaseCommand
from faker import Faker
from onboarding.models import Customeruser

class Command(BaseCommand):
    help = 'Populates the database with fake Customeruser data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(50):
            Customeruser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='defaultpass123',
                phone_no=fake.phone_number(),
                is_staff=fake.boolean(chance_of_getting_true=30)
            )
        self.stdout.write(self.style.SUCCESS("Successfully populated fake users."))
