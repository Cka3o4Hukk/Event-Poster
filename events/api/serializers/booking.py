from rest_framework import serializers

from events.domain.models.booking import Booking
from events.domain.models.event import Event


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Booking
        fields = ('id', 'user', 'event', 'created_at')
        read_only_fields = ('id', 'created_at', 'user')
