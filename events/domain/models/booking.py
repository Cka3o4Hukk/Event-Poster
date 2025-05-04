from django.contrib.auth.models import User
from django.db import models

from events.domain.models.event import Event


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings')
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self) -> str:
        return f"{self.user.username} - {self.event.title}"
