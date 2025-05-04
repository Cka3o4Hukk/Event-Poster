from django.core.exceptions import ValidationError

from events.domain.models import Booking, Event
from events.domain.tasks import notify_user


class BookingService:
    @staticmethod
    def create_booking(user, event: Event) -> Booking:
        """Создает бронирование с валидацией."""
        if Booking.objects.filter(user=user, event=event).exists():
            raise ValidationError("Вы уже забронировали место.")

        if not event.is_booking:
            raise ValidationError("Бронирование закрыто.")

        if Booking.objects.filter(event=event).count() >= event.seats:
            raise ValidationError("Нет свободных мест.")

        booking = Booking.objects.create(user=user, event=event)
        notify_user.delay(
            user.id,
            event.id,
            f"Вы забронировали мероприятие: {event.title}")
        return booking

    @staticmethod
    def cancel_booking(booking: Booking) -> None:
        """Отменяет бронирование и отправляет уведомление."""
        notify_user.delay(
            booking.user.id,
            booking.event.id,
            f"Вы отменили бронирование для мероприятия: {booking.event.title}")
        booking.delete()
