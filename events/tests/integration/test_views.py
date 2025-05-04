from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from events.domain.models import Booking, Event, Rating


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
    )


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username='admin',
        password='adminpassword',
        email='admin@example.com',
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
def past_event(user):
    return Event.objects.create(
        title='Past Event',
        description='Past description',
        start_time=timezone.now() - timedelta(days=1),
        location='Test City',
        seats=50,
        status='completed',
        organizer=user,
    )


@pytest.mark.django_db
def test_event_list(api_client, event, past_event):
    response = api_client.get('/api/v1/events/')
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 2
    assert data[0]['id'] == event.id
    assert data[1]['id'] == past_event.id


@pytest.mark.django_db
def test_event_create(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'title': 'New Event',
        'description': 'New description',
        'start_time': '2025-05-10T14:00:00Z',
        'location': 'New City',
        'seats': 50,
    }
    response = api_client.post('/api/v1/events/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1
    assert Event.objects.first().title == 'New Event'


@pytest.mark.django_db
def test_event_update(api_client, event, user):
    api_client.force_authenticate(user=user)
    data = {
        'title': 'Updated Event',
        'description': event.description,
        'start_time': event.start_time,
        'location': event.location,
        'seats': event.seats,
        'status': event.status,
    }
    response = api_client.put(f'/api/v1/events/{event.id}/', data)
    assert response.status_code == status.HTTP_200_OK
    event.refresh_from_db()
    assert event.title == 'Updated Event'


@pytest.mark.django_db
def test_event_delete(api_client, event, user):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/v1/events/{event.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_booking_create(api_client, event, user):
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/v1/bookings/', {'event': event.id},
                               format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.count() == 1
    booking = Booking.objects.first()
    assert booking.user == user
    assert booking.event == event


@pytest.mark.django_db
def test_rating_create(api_client, event, user):
    api_client.force_authenticate(user=user)
    Booking.objects.create(user=user, event=event)
    event.status = 'completed'
    event.save()

    data = {'event': event.id, 'score': 5}
    response = api_client.post('/api/v1/ratings/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.count() == 1
    rating = Rating.objects.first()
    assert rating.user == user
    assert rating.event == event
    assert rating.score == 5


@pytest.mark.django_db
def test_create_rating(api_client, user, past_event):
    Booking.objects.create(user=user, event=past_event)
    api_client.force_authenticate(user=user)
    url = '/api/v1/ratings/'
    data = {'event': past_event.id, 'score': 4}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.filter(user=user, event=past_event, score=4).exists()


@pytest.mark.django_db
def test_rating_rejected_for_planned_event(api_client, user, event):
    api_client.force_authenticate(user=user)
    url = '/api/v1/ratings/'
    data = {'event': event.id, 'score': 4}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Можно оценивать только завершенные события' in str(response.data)


@pytest.mark.django_db
def test_rating_rejected_for_non_participant(api_client, user, past_event):
    api_client.force_authenticate(user=user)
    url = '/api/v1/ratings/'
    data = {'event': past_event.id, 'score': 4}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Можно оценивать только свои посещенные события' in str(
        response.data)


@pytest.mark.django_db
def test_event_list_sorted_by_rating(api_client, user, past_event):
    api_client.force_authenticate(user=user)
    Booking.objects.create(user=user, event=past_event)
    Rating.objects.create(user=user, event=past_event, score=5)
    response = api_client.get('/api/v1/events/?ordering=-avg_rating')
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) >= 1
    assert data[0]['id'] == past_event.id
