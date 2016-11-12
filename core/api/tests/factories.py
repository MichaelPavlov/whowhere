import factory
from django.contrib.auth.models import User
from faker import Factory

from core.api.tests.faker_providers import TechDataProvider, DateProvider
from core.models import Event, City, Station, Place, PlaceCategory, PlaceSubcategory, EventSubcategory, EventCategory, \
    Tag, TagCategory

faker = Factory.create('ru_RU')
faker.add_provider(TechDataProvider)
faker.add_provider(DateProvider)


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.LazyAttribute(lambda x: faker.city())
    timezone_string = factory.LazyAttribute(lambda x: faker.timezone())


class StationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Station

    city = factory.SubFactory(CityFactory)
    name = factory.LazyAttribute(lambda x: faker.name())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user-%d' % n)
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())


class TagCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TagCategory

    name = factory.LazyAttribute(lambda x: faker.company())
    icon = factory.django.ImageField()


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda x: faker.company())
    category = factory.SubFactory(TagCategoryFactory)
    icon = factory.django.ImageField()


class PlaceCategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlaceCategory

    name = factory.LazyAttribute(lambda x: faker.place_category())


class PlaceSubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlaceSubcategory

    name = factory.LazyAttribute(lambda x: faker.place_subcategory())
    category = factory.SubFactory(PlaceCategoryFactory)


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Place

    title = factory.LazyAttribute(lambda x: faker.place_title())
    category = factory.SubFactory(PlaceCategoryFactory)
    city = factory.SubFactory(CityFactory)
    description = factory.LazyAttribute(lambda x: faker.text())
    misc = factory.LazyAttribute(lambda x: faker.text())
    image = factory.django.ImageField(color='blue')
    address = factory.LazyAttribute(lambda x: faker.address())
    station = factory.SubFactory(StationFactory)
    link = factory.LazyAttribute(lambda x: faker.uri())
    buy_link = factory.LazyAttribute(lambda x: faker.uri())
    price = factory.LazyAttribute(lambda x: faker.integer_range())
    price_unknown = factory.LazyAttribute(lambda x: faker.pybool())
    time_unknown = factory.LazyAttribute(lambda x: faker.pybool())
    views = factory.LazyAttribute(lambda x: faker.pyint())
    visitors_count = factory.LazyAttribute(lambda x: faker.pyint())
    rating = factory.LazyAttribute(lambda x: faker.pyint())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    website = factory.LazyAttribute(lambda x: faker.url())
    point = factory.LazyAttribute(lambda x: faker.geo_point())

    @factory.post_generation
    def subcats(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for subcat in extracted:
                self.subcats.add(subcat)

    @factory.post_generation
    def favorited_by(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.favorited_by.add(user)

    @factory.post_generation
    def wished_by(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.wished_by.add(user)


class EventCategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = EventCategory

    name = factory.LazyAttribute(lambda x: faker.event_category())


class EventSubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = EventSubcategory

    name = factory.LazyAttribute(lambda x: faker.event_subcategory())
    category = factory.SubFactory(EventCategoryFactory)


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.LazyAttribute(lambda x: faker.place_title())
    description = factory.LazyAttribute(lambda x: faker.text())
    address = factory.LazyAttribute(lambda x: faker.address())
    city = factory.SubFactory(CityFactory)
    station = factory.SubFactory(StationFactory)
    point = factory.LazyAttribute(lambda x: faker.geo_point())
    organizer = factory.SubFactory(UserFactory)
    status = factory.LazyAttribute(lambda x: faker.pybool())
    place = factory.SubFactory(PlaceFactory)
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    price = factory.LazyAttribute(lambda x: faker.integer_range())
    participants = factory.LazyAttribute(lambda x: faker.pyint())
    price_unknown = factory.LazyAttribute(lambda x: faker.pybool())
    is_free = factory.LazyAttribute(lambda x: faker.pybool())
    time_unknown = factory.LazyAttribute(lambda x: faker.pybool())
    time_all = factory.LazyAttribute(lambda x: faker.pybool())
    schedule = factory.LazyAttribute(lambda x: faker.schedule())
    dates = factory.LazyAttribute(lambda x: faker.date_ranges_list())
    days = factory.LazyAttribute(lambda x: faker.days())
    public = factory.LazyAttribute(lambda x: faker.pybool())
    is_recurring = factory.LazyAttribute(lambda x: faker.pybool())
    views = factory.LazyAttribute(lambda x: faker.pyint())
    rating = factory.LazyAttribute(lambda x: faker.pyint())
    website = factory.LazyAttribute(lambda x: faker.url())
    image_source = factory.LazyAttribute(lambda x: faker.uri())
    link = factory.LazyAttribute(lambda x: faker.uri())
    misc = factory.LazyAttribute(lambda x: faker.text())
    min_age = factory.LazyAttribute(lambda x: faker.pyint())

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def subcategories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for subcategory in extracted:
                self.subcategories.add(subcategory)

    @factory.post_generation
    def favorited_by(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.favorited_by.add(user)

    @factory.post_generation
    def wished_by(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.wished_by.add(user)
