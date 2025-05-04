from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from events.domain.models import Event


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
    )


@pytest.mark.django_db
class TestAPIAccessMiddleware:
    def test_get_request_allowed_without_auth(self, api_client):
        """GET запросы должны быть доступны без аутентификации."""
        url = reverse('event-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_post_request_requires_auth(self, api_client):
        """POST запросы должны требовать аутентификацию."""
        url = reverse('event-list')
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'start_time': '2024-03-20T15:00:00Z',
            'seats': 10}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()[
            'error'] == 'Требуется аутентификация для доступа к API'

    def test_post_request_allowed_with_auth(self, api_client, user):
        """POST запросы должны быть разрешены с аутентификацией."""
        api_client.force_authenticate(user=user)
        url = reverse('event-list')
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'start_time': '2024-03-20T15:00:00Z',
            'seats': 10}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_put_request_requires_auth(self, api_client, user):
        """PUT запросы должны требовать аутентификацию."""
        api_client.force_authenticate(user=user)
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            location='Test Location',
            start_time='2024-03-20T15:00:00Z',
            seats=10,
            organizer=user,
        )
        api_client.force_authenticate(user=None)

        url = reverse('event-detail', args=[event.id])
        data = {'title': 'Updated Event'}
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()[
            'error'] == 'Требуется аутентификация для доступа к API'

    def test_delete_request_requires_auth(self, api_client, user):
        """DELETE запросы должны требовать аутентификацию."""
        api_client.force_authenticate(user=user)
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            location='Test Location',
            start_time='2024-03-20T15:00:00Z',
            seats=10,
            organizer=user,
        )
        api_client.force_authenticate(user=None)

        url = reverse('event-detail', args=[event.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()[
            'error'] == 'Требуется аутентификация для доступа к API'
