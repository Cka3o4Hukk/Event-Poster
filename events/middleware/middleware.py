from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authentication import get_authorization_header


class APIAccessMiddleware:
    """Middleware для проверки доступа к API endpoints."""

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Проверяет доступ к API endpoints."""
        if request.path.startswith('/api/'):
            if request.method != 'GET':
                is_authenticated = (
                    request.user.is_authenticated or
                    bool(get_authorization_header(request)) or
                    getattr(request, '_force_auth_user', None) is not None
                )

                if not is_authenticated:
                    return JsonResponse(
                        {'error':
                         'Требуется аутентификация для доступа к API'},
                        status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response
