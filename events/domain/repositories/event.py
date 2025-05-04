from django.db.models import Avg, Case, Count, IntegerField, Q, Value, When
from django.utils import timezone

from events.domain.models import Event


class EventRepository:
    @staticmethod
    def get_annotated_events():
        now = timezone.now()
        return Event.objects.annotate(
            avg_rating=Avg('ratings__score'),
            booked=Count('bookings'),
            sort_order=Case(
                When(status='planned', start_time__gte=now, then=Value(1)),
                When(~Q(status='planned'), then=Value(2)),
                default=Value(3),
                output_field=IntegerField())).order_by(
            'sort_order', 'start_time')

    @staticmethod
    def delete_event(event: Event) -> None:
        """Удаляет событие."""
        event.delete()
