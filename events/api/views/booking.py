from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.api.mixins.error_handling import ErrorHandlingMixin
from events.api.serializers import BookingSerializer
from events.domain.models import Booking
from events.domain.services.booking import BookingService


class BookingViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    """Управление бронированиями."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event = serializer.validated_data["event"]
        BookingService.create_booking(self.request.user, event)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_booking(self, request, pk=None):
        """Отменяет бронирование."""
        booking = self.get_object()
        BookingService.cancel_booking(booking)
        return Response(status=204)
