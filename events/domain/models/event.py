from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Event(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'planned', 'Ожидается'
        CANCELED = 'canceled', 'Отменено'
        COMPLETED = 'completed', 'Завершено'
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    seats = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED)
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        'events.Tag',
        related_name='events',
        blank=True)

    @property
    def is_booking(self) -> bool:
        """Проверяет, можно ли забронировать место на событие. """
        time_left = self.start_time - timezone.now()
        is_time_valid = time_left > timedelta(minutes=30)
        is_status_valid = self.status == self.StatusChoices.PLANNED
        return is_time_valid and is_status_valid

    def __str__(self) -> str:
        return self.title
