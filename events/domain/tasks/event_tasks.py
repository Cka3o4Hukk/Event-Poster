import logging

from celery import shared_task
from django.utils import timezone

from events.domain.models import Event

logger = logging.getLogger(__name__)


@shared_task
def complete_old_events() -> None:
    now = timezone.now()
    outdated_events = Event.objects.filter(
        status="planned",
        start_time__lt=now - timezone.timedelta(hours=2),
    )
    if outdated_events.exists():
        for event in outdated_events:
            event.status = "completed"
            event.save()
    else:
        logger.error("[COMPLETE EVENTS] No outdated events found.")
        return
