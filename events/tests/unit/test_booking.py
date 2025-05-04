import pytest
from django.contrib.auth.models import User

from events.domain.models import Booking, Event


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
        start_time='2025-05-10T14:00:00Z',
        location='Test City',
        seats=100,
        status='planned',
        organizer=user)


@pytest.mark.django_db
def test_booking_create(user, event):
    booking = Booking.objects.create(user=user, event=event)
    assert booking.user == user
    assert booking.event == event


@pytest.mark.django_db
def test_booking_unique(user, event):
    Booking.objects.create(user=user, event=event)
    with pytest.raises(Exception):
        Booking.objects.create(user=user, event=event)
