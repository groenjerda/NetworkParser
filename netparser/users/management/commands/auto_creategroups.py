from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание групп для кандидатов и подтвержденных пользователей'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name=settings.CANDIDATE_GROUP)
        Group.objects.get_or_create(name=settings.USERS_GROUP)
        self.style.SUCCESS('Groups created')
