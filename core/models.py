from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import ArrayField, DateRangeField, IntegerRangeField, JSONField

from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField


class EventCategory(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории событий'
        verbose_name = 'Категория событий'


class EventSubcategory(models.Model):
    name = models.CharField(max_length=75)
    category = models.ForeignKey(EventCategory)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Подкатегории событиый'
        verbose_name = 'Подкатегория событий'


class TagCategory(models.Model):
    name = models.CharField(max_length=75)
    icon = models.ImageField(upload_to='tag_images', blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=75)
    category = models.ForeignKey(TagCategory)
    icon = models.ImageField(upload_to='tag_images', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название города')
    timezone_string = models.CharField(max_length=50, default='Europe/Moscow')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'


class Place(models.Model):
    title = models.CharField(max_length=75, verbose_name='Заголовок')
    category = models.ForeignKey('PlaceCategory', verbose_name='Категория')
    subcats = ChainedManyToManyField(
        'PlaceSubcategory',
        chained_field='category',
        chained_model_field='category',
        verbose_name='Подкатегории',
        blank=True,
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    misc = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')
    image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name='Картинка')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    city = models.ForeignKey(City, verbose_name='Город')
    station = ChainedForeignKey(
        Station,
        chained_field="city",
        chained_model_field="city",
        show_all=False,
        auto_choose=True,
        blank=True,
        null=True,
        verbose_name='Станции метро'
    )
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка на источник фотографий')
    buy_link = models.TextField(blank=True, null=True, verbose_name='Ссылка на покупку билета')
    price = IntegerRangeField(blank=True, null=True)
    price_unknown = models.BooleanField(default=False, verbose_name='Цена неопределена')
    time_unknown = models.BooleanField(default=False, verbose_name='Время неопределено')
    views = models.IntegerField(blank=True, null=True, default=0)
    visitors_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    website = models.CharField(max_length=254, blank=True, null=True)
    point = geomodels.PointField(geography=True, blank=True, null=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_places', blank=True)
    wished_by = models.ManyToManyField(User, related_name='wishlist_places', blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=75, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    subcategories = models.ManyToManyField(EventSubcategory, blank=True)
    city = models.ForeignKey(City, verbose_name='Город')
    station = ChainedForeignKey(
        Station,
        chained_field="city",
        chained_model_field="city",
        show_all=False,
        auto_choose=True,
        blank=True,
        null=True,
        verbose_name='Станции метро'
    )
    point = geomodels.PointField(blank=True, null=True)
    organizer = models.ForeignKey(User, blank=True, null=True, related_name='events_set')
    status = models.BooleanField(default=False)
    place = models.ForeignKey(Place, blank=True, null=True, verbose_name='Место')
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Телефон')
    price = IntegerRangeField(blank=True, null=True, verbose_name='Цена')
    participants = models.IntegerField(default=0, verbose_name='Участники')
    price_unknown = models.BooleanField(default=False, verbose_name='Цена неопроеделена')
    is_free = models.BooleanField(default=False, verbose_name='Бесплатное событие')
    time_unknown = models.BooleanField(default=False, verbose_name='Время неопределено')
    time_all = models.BooleanField(default=False, verbose_name='Круглосуточно каждый день')
    schedule = JSONField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    dates = ArrayField(DateRangeField(), blank=True, null=True)
    days = ArrayField(models.DateTimeField(), blank=True, null=True)
    public = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False, verbose_name='Повторяющееся событие')
    views = models.IntegerField(blank=True, null=True, default=0, verbose_name='Просмотры')
    rating = models.IntegerField(default=5, blank=True, null=True, verbose_name='Рейтинг')
    website = models.CharField(max_length=255, blank=True, null=True, verbose_name='Сайт')
    image_source = models.CharField(max_length=255, blank=True, null=True, verbose_name='Источник фото')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')
    misc = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')
    min_age = models.IntegerField(blank=True, null=True, verbose_name='Минимальный возраст')
    favorited_by = models.ManyToManyField(User, related_name='favorite_events', blank=True)
    wished_by = models.ManyToManyField(User, related_name='wishlist_events', blank=True)

    def __str__(self):
        return self.title


class PlaceCategory(models.Model):
    name = models.CharField(max_length=75, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория мест'
        verbose_name_plural = 'Категории мест'


class PlaceSubcategory(models.Model):
    name = models.CharField(max_length=75, verbose_name='Название подкатегории')
    category = models.ForeignKey(PlaceCategory)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория мест'
        verbose_name_plural = 'Подкатегории мест'
