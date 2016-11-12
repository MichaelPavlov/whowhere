from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from core.api.views.event_views import EventViewSet

router = SimpleRouter(trailing_slash=False)
# router.register(r'pictures', PictureViewSet, base_name='picture')
# router.register(r'visits', VisitViewSet, base_name='visit')
# router.register(r'places', PlaceViewSet, base_name='place')
router.register(r'events', EventViewSet, base_name='event')

urlpatterns = [
    url(r'^', include(router.urls)),
]
