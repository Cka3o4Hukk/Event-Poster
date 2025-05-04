from datetime import timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from events.domain.models import Event


class EventService:
    @staticmethod
    def validate_organizer(user, event: Event) -> None:
        """Проверяет, является ли пользователь организатором."""
        if event.organizer != user:
            raise PermissionDenied("Доступно только организатору.")

    @staticmethod
    def validate_deletion_time(event: Event) -> None:
        """Проверяет, можно ли удалить событие."""
        if timezone.now() - event.created_at > timedelta(hours=1):
            raise ValidationError(
                "Удаление доступно в течение 1 часа после создания.")

    @staticmethod
    def validate_status(new_status: str) -> None:
        """Проверяет допустимость статуса."""
        if new_status not in dict(Event.STATUS_CHOICES):
            raise ValidationError("Недопустимый статус.")

    @staticmethod
    def update_event_status(event: Event, user, new_status: str) -> Event:
        """Обновляет статус события."""
        EventService.validate_organizer(user, event)
        EventService.validate_status(new_status)
        event.status = new_status
        event.save()
        return event
