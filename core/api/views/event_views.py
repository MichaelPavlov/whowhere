# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import EventSerializer, EventsPageDataSerializer
from core.models import Event


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [AllowAny]


class EventsPageDataView(APIView):
    def get(self, request):
        qs_data = {
            'events': Event.objects.all()[:5],
            # 'categories': EventSubcategory.objects.all()[:5],
        }

        serializer = EventsPageDataSerializer(qs_data)
        return Response(serializer.data)
