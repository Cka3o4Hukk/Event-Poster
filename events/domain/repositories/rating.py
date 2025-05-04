from django.db.models.query import QuerySet

from events.domain.models import Rating


class RatingRepository:
    @staticmethod
    def get_user_ratings(user) -> QuerySet[Rating]:
        """Возвращает все оценки текущего пользователя."""
        return Rating.objects.filter(user=user)

    @staticmethod
    def create_rating(user, event, score: int) -> Rating:
        """Создает новую оценку."""
        return Rating.objects.create(user=user, event=event, score=score)
