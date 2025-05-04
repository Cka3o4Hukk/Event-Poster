from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.api.views import (
    BookingViewSet,
    EventViewSet,
    NotificationViewSet,
    RatingViewSet,
)

router: DefaultRouter = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
