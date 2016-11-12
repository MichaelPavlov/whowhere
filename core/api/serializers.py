# -*- coding: utf-8 -*-
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from core.models import Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    dates = SerializerMethodField()

    def get_dates(self, obj):
        pass
        return []


class EventsPageDataSerializer(Serializer):
    events = SerializerMethodField()

    # filters = SerializerMethodField()

    def get_events(self, obj):
        return EventSerializer(self.instance['events'], many=True).data

    def get_filters(self, obj):
        pass
