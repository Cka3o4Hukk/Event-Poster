from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.db.models import Avg, Count, F
from django.utils import timezone
from rest_framework.test import APIClient

from events.domain.models import Booking, Event, Rating, Tag


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
    )


@pytest.fixture
def api_client():
    return APIClient()


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
def booked_event(user):
    event = Event.objects.create(
        title='Booked Event',
        description='Booked description',
        start_time=timezone.now() + timedelta(days=1),
        location='Test City',
        seats=2,
        status='planned',
        organizer=user,
    )
    Booking.objects.create(user=user, event=event)
    return event


@pytest.fixture
def rated_event(user):
    event = Event.objects.create(
        title='Rated Event',
        description='Rated description',
        start_time=timezone.now() - timedelta(days=1),
        location='Test City',
        seats=50,
        status='completed',
        organizer=user,
    )
    Booking.objects.create(user=user, event=event)
    Rating.objects.create(user=user, event=event, score=4)
    return event


@pytest.fixture
def events(user):
    now = timezone.now()
    tag1 = Tag.objects.create(name='tag1')
    tag2 = Tag.objects.create(name='tag2')

    event1 = Event.objects.create(
        title='Past Event',
        description='Test description',
        start_time=now - timedelta(days=1),
        location='Test City',
        seats=100,
        status='completed',
        organizer=user)
    event1.tags.add(tag1)

    event2 = Event.objects.create(
        title='Future Event',
        description='Test description',
        start_time=now + timedelta(days=1),
        location='Test City',
        seats=100,
        status='planned',
        organizer=user)
    event2.tags.add(tag2)

    return [event1, event2]


@pytest.mark.django_db
def test_event_filter_by_location(event):
    events = Event.objects.filter(location='Test City')
    assert len(events) > 0
    assert event in events


@pytest.mark.django_db
def test_event_filter_by_date(event):
    events = Event.objects.filter(start_time__gte=timezone.now())
    assert len(events) > 0
    assert event in events


@pytest.mark.django_db
def test_event_filter_by_status(api_client, events):
    response = api_client.get('/api/v1/events/', {'status': 'planned'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Future Event'


@pytest.mark.django_db
def test_event_filter_by_free_seats(event):
    events = Event.objects.annotate(booked=Count('bookings')).filter(
        booked__lt=F('seats'))
    assert len(events) > 0
    assert event in events


@pytest.mark.django_db
def test_event_filter_by_booked_seats(booked_event):
    events = Event.objects.annotate(booked=Count('bookings')).filter(
        booked__gte=F('seats'))
    assert len(events) == 0
    events = Event.objects.annotate(booked=Count('bookings')).filter(
        booked__lt=F('seats'))
    assert booked_event in events


@pytest.mark.django_db
def test_event_filter_by_rating(rated_event, user):
    events = Event.objects.annotate(avg_rating=Avg('ratings__score')).filter(
        avg_rating__gte=3)
    assert len(events) > 0
    assert rated_event in events


@pytest.mark.django_db
def test_event_filter_by_tag(api_client, events):
    tag = Tag.objects.get(name='tag1')
    response = api_client.get(f'/api/v1/events/?tags={tag.id}')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Past Event'
