from rest_framework import serializers

from events.domain.models.rating import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'event', 'user', 'score', 'created_at')
        read_only_fields = ('user', 'created_at')
