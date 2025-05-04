from rest_framework import serializers

from events.domain.models.event import Event
from events.domain.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'event', 'message', 'created_at')
        read_only_fields = ('id', 'created_at', 'user', 'event', 'message')
