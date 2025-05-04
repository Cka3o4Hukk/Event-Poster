from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.api.filters.filters import EventFilter
from events.api.serializers import EventSerializer
from events.domain.models import Event
from events.domain.repositories.event import EventRepository


class EventViewSet(viewsets.ModelViewSet):
    """Управление событиями (только CRUD операции)."""

    queryset = EventRepository.get_annotated_events()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    http_method_names = ["get", "post", "put", "delete"]

    def perform_destroy(self, instance):
        """Удаление события с валидацией."""
        from events.domain.services.event import EventService

        EventService.validate_organizer(self.request.user, instance)
        EventService.validate_deletion_time(instance)
        super().perform_destroy(instance)

    @action(detail=True, methods=["put"], url_path="status")
    def update_status(self, request, pk=None):
        """Обновление статуса события."""
        event = self.get_object()
        status_value = request.data.get("status")

        if status_value not in Event.StatusChoices.values:
            return Response(
                {"error": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST)

        event.status = status_value
        event.save()
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
