from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from events.domain.models import Booking, Event, Tag


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


@pytest.mark.django_db
def test_event_str(event):
    assert str(event) == 'Test Event'


@pytest.mark.django_db
def test_event_is_booking(event):
    assert event.is_booking is True
    event.status = 'completed'
    event.save()
    assert event.is_booking is False


@pytest.mark.django_db
def test_event_tags(event):
    tag = Tag.objects.create(name='test_tag')
    event.tags.add(tag)
    assert tag in event.tags.all()
    assert str(tag) == 'test_tag'


@pytest.mark.django_db
def test_event_creation(event):
    assert event.title == 'Test Event'
    assert event.status == 'planned'


@pytest.mark.django_db
def test_booking_creation(user, event):
    booking = Booking.objects.create(user=user, event=event)
    assert booking.user == user
    assert booking.event == event
