from django.db.models.query import QuerySet

from events.domain.models import Booking


class BookingRepository:
    @staticmethod
    def get_user_bookings(user) -> QuerySet[Booking]:
        """Возвращает бронирования пользователя."""
        return Booking.objects.filter(user=user)

    @staticmethod
    def create_booking(user, event) -> Booking:
        """Создает новое бронирование."""
        return Booking.objects.create(user=user, event=event)

    @staticmethod
    def delete_booking(booking: Booking) -> None:
        """Удаляет бронирование."""
        booking.delete()
