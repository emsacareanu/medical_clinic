# myapp/management/commands/create_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import AppointmentsModel

class Command(BaseCommand):
    help = 'Create regular users for testing'

    def handle(self, *args, **kwargs):
        user = AppointmentsModel.objects.create_user('claudiu', 'claudiu@gmail.com', 'receptionist')
        user.first_name = 'Regular'
        user.last_name = 'User'
        user.save()

        self.stdout.write(self.style.SUCCESS('Regular user created successfully.'))
