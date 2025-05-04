from django.contrib.auth.models import User
from django.db import models

from events.domain.models.event import Event


class Rating(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ratings')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings')
    score = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self) -> str:
        return f"{self.user.username} - {self.event.title} ({self.score})"
