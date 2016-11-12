# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from core.api.tests.factories import CityFactory, StationFactory, UserFactory, PlaceFactory
from core.models import City, Event


class EventModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.city = CityFactory()
        cls.station = StationFactory()
        cls.user = UserFactory()
        cls.place = PlaceFactory()

        cls.event1 = Event(
            title="Концерт Боба Дилана",
            description="На сцене Рахманиновского зала Консерватории выступит заслуженный деятель искусств США, Боб Дилан",
            address="ул., Ушинского 15",
            city=cls.city,
            station=cls.station,
            point=GEOSGeometry('POINT(5 23)'),
            organizer=cls.user,
            status=True,
            place=cls.place,
            phone="+79781125620",
            price=(100, 1000),
            participants=10,
            price_unknown=False,
            is_free=False,
            time_unknown=False,
            time_all=False,
            schedule={"all": "", "friday": {"to": "21:00", "from": "11:00", "enable": True},
                      "monday": {"to": "21:00", "from": "11:00", "enable": True},
                      "sunday": {"to": "21:00", "from": "10:00", "enable": True},
                      "tuesday": {"to": "21:00", "from": "11:00", "enable": True},
                      "saturday": {"to": "21:00", "from": "10:00", "enable": True},
                      "thursday": {"to": "21:00", "from": "11:00", "enable": True},
                      "wednesday": {"to": "21:00", "from": "11:00", "enable": True}},
            add_date=datetime.now(),
            dates={"[2016-06-26,2016-07-07)", "[2016-07-17,2016-07-28)"},
            days={'2016-09-15 19:00:00.000000', '2016-11-26 18:00:00.000000'},
            public=True,
            is_recurring=False,
            views=1000,
            rating=5,
            website="http://crimea-bowling.ru",
            image_source="BBC",
            link="http://bing.com",
            misc='Дополнительная информация',
            min_age=13,

        )

    def test_event_basic(self):
        """
        Test the basic functionality of Event model
        """
        self.assertEqual(self.event1.phone, "+79781125620")
        self.assertEqual(self.event1.views, 1000)


class CityModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.city = City(
            name='Симферополь',
            timezone_string='Europe/Kiev'
        )

    def test_event_basic(self):
        """
        Test the basic functionality of City model
        """
        self.assertEqual(self.city.name, 'Симферополь')
        self.assertEqual(self.city.timezone_string, 'Europe/Kiev')
