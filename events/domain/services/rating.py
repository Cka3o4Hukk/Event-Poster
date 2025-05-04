from rest_framework.exceptions import ValidationError

from events.domain.models import Booking, Event


class RatingService:
    @staticmethod
    def validate_rating(user, event: Event) -> None:
        if event.status != 'completed':
            raise ValidationError(
                "Можно оценивать только завершенные события.")

        if not Booking.objects.filter(user=user, event=event).exists():
            raise ValidationError(
                "Можно оценивать только свои посещенные события.")
