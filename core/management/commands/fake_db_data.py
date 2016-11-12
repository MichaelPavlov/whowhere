from django.core.management.base import BaseCommand
from core.api.tests.factories import *


class Command(BaseCommand):
    help = 'Populates database with fake data'

    def handle(self, *args, **options):
        tags = TagFactory.create_batch(3)
        event_subcategories = EventSubcategoryFactory.create_batch(3)
        users = UserFactory.create_batch(5)
        events = EventFactory.create_batch(3, tags=tags, subcategories=event_subcategories,
                                           favorited_by=users[3:],
                                           wished_by=users[:2])
