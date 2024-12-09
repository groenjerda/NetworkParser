from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание суперпользователя с заданными параметрами'

    def handle(self, *args, **options):
        if User.objects.filter(username=settings.SUPERUSER_NAME).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
        else:
            User.objects.create_superuser(
                username=settings.SUPERUSER_NAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASS
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
