from django.db.models.query import QuerySet
from rest_framework import permissions, serializers, viewsets
from rest_framework.exceptions import ValidationError

from events.api.serializers import RatingSerializer
from events.domain.models import Rating
from events.domain.repositories.rating import RatingRepository
from events.domain.services.rating import RatingService


class RatingViewSet(viewsets.ModelViewSet):
    """Управление оценками событий."""
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self) -> QuerySet[Rating]:
        """Возвращает оценки текущего пользователя."""
        return RatingRepository.get_user_ratings(self.request.user)

    def perform_create(self, serializer: RatingSerializer) -> None:
        """Создает оценку с валидацией через сервис."""
        event = serializer.validated_data['event']
        score = serializer.validated_data['score']

        try:
            RatingService.validate_rating(self.request.user, event)
            RatingRepository.create_rating(
                user=self.request.user,
                event=event,
                score=score)
        except ValidationError as e:
            raise serializers.ValidationError(e.detail) from e

