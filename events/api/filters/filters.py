import logging
from typing import Optional

import django_filters
from django.db.models import Avg, Count, F, QuerySet

from events.domain.models import Event, Tag

logger = logging.getLogger(__name__)


class EventFilter(django_filters.FilterSet):
    available = django_filters.BooleanFilter(method='filter_available')
    avg_rating = django_filters.NumberFilter(
        field_name='avg_rating',
        lookup_expr='gte')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all(),
        conjoined=True)

    class Meta:
        model = Event
        fields = {
            'location': ('exact',),
            'status': ('exact',),
            'start_time': ('gte', 'lte'),
            'seats': ('exact', 'gte', 'lte'),
        }

    def filter_queryset(self, queryset: QuerySet[Event]) -> QuerySet[Event]:
        """Аннотирует queryset средней оценкой и количеством бронирований."""
        queryset = queryset.annotate(
            avg_rating=Avg('ratings__score'),
            booked=Count('bookings'))
        try:
            return super().filter_queryset(queryset)
        except Exception as e:
            logger.warning(f"Ошибка фильтрации: {e!s}")
            return queryset.none()

    def filter_available(self, queryset: QuerySet[Event],
                         name: str, value: bool) -> QuerySet[Event]:
        """Фильтрует события по доступности мест."""
        if value:
            return queryset.filter(booked__lt=F("seats"))
        return queryset.filter(booked__gte=F("seats"))

    def filter_avg_rating_gte(self,
                              queryset: QuerySet[Event],
                              value: Optional[float]) -> QuerySet[Event]:
        """Фильтрует события по средней оценке (>=)."""
        if value is not None:
            return queryset.filter(avg_rating__gte=value)
        return queryset
