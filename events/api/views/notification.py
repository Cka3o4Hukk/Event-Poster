from django.db.models.query import QuerySet
from rest_framework import permissions, viewsets

from events.api.serializers import NotificationSerializer
from events.domain.models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet[Notification]:
        return Notification.objects.filter(user=self.request.user)
