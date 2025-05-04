import logging

from celery import shared_task
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from events.domain.models import Event, Notification

logger = logging.getLogger(__name__)


@shared_task
def notify_user(user_id: int, event_id: int, message: str) -> None:
    logger.info(f"[STARTING TASK] Notify user {user_id} for event {event_id}")
    try:
        user = User.objects.get(pk=user_id)
        event = Event.objects.get(pk=event_id)
        Notification.objects.create(user=user, event=event, message=message)
        logger.info(f"[NOTIFY] {user.username}: {message}")
    except ObjectDoesNotExist as e:
        logger.error(f"[ERROR] Object not found: {e}")
        return
