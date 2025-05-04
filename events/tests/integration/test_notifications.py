from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from events.domain.models import Booking, Event, Notification


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
    )


@pytest.fixture
def event(user):
    return Event.objects.create(
        title='Test Event',
        description='Test description',
        start_time=timezone.now() + timedelta(days=1),
        location='Test City',
        seats=100,
        status='planned',
        organizer=user,
    )


@pytest.fixture
def mock_notify_user():
    with patch('events.tasks.notify_user.delay') as mock:
        yield mock


@pytest.mark.django_db
@patch('events.domain.services.booking.notify_user.delay')
def test_booking_notification(mock_notify_user, client, user, event):
    client.login(username='testuser', password='testpassword')
    url = '/api/v1/bookings/'
    data = {'event': event.id}
    response = client.post(url, data, content_type='application/json')
    
    assert response.status_code == 201
    mock_notify_user.assert_called_once_with(
        user.id,
        event.id,
        'Вы забронировали мероприятие: Test Event',
    )


@pytest.mark.django_db
@patch('events.domain.services.booking.notify_user.delay')
def test_cancel_booking_notification(mock_notify_user, client, user, event):
    booking = Booking.objects.create(user=user, event=event)
    client.login(username='testuser', password='testpassword')

    url = f'/api/v1/bookings/{booking.id}/cancel/'
    response = client.post(url)

    assert response.status_code == 204
    mock_notify_user.assert_called_once_with(
        user.id,
        event.id,
        'Вы отменили бронирование для мероприятия: Test Event',
    )


@pytest.mark.django_db
def test_notification_str(user, event):
    notification = Notification.objects.create(
        user=user,
        event=event,
        message='Test notification')
    assert str(notification) == 'Notification for testuser: Test notification'
