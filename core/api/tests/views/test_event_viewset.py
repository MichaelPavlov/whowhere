from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from core.api.tests.factories import EventFactory, TagFactory, EventSubcategoryFactory, UserFactory
from core.models import Event


class EventViewSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tags = TagFactory.create_batch(3)
        cls.event_subcategories = EventSubcategoryFactory.create_batch(3)
        cls.users = UserFactory.create_batch(5)
        cls.events = EventFactory.create_batch(3, tags=cls.tags, subcategories=cls.event_subcategories,
                                               favorited_by=cls.users[3:],
                                               wished_by=cls.users[:2])

    def test_event_list_view_has_tree_objects(self):
        """
        Test that list view has 3 objects
        """
        url = reverse('api:event-list')
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 3)

    def test_event_retrieve_view_set(self):
        """
        Test that event retrieve returns 200 status code
        """
        url = reverse('api:event-detail', kwargs={"pk": self.events[0].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete_view_set(self):
        """
        Test that event can be deleted
        """
        url = reverse('api:event-detail', kwargs={"pk": self.events[0].id})
        response = self.client.delete(url)

        self.assertFalse(Event.objects.filter(id=self.events[0].id).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_event_create_view_set(self):
        """
        Test that event can be created
        """
        data = {

        }
        url = reverse('api:event-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
