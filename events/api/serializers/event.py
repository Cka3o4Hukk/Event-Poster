from typing import Any, Dict

from django.contrib.auth.models import User
from rest_framework import serializers

from events.api.serializers.tag import TagSerializer
from events.domain.models.event import Event
from events.domain.models.tag import Tag


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='organizer',
        write_only=True,
        required=False)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False)

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'start_time', 'location', 'seats',
            'status', 'organizer', 'organizer_id', 'created_at', 'tags',
            'tag_ids')
        read_only_fields = ('id', 'created_at', 'organizer')

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return super().validate(data)

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance: Event, validated_data: Dict[str, Any]) -> Event:
        tags = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)
        return instance
