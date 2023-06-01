from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Create user profiles for existing users'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS('User profiles created successfully.'))