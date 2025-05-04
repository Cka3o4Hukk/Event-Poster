from rest_framework.response import Response


class ErrorHandlingMixin:
    def create_error_response(self, detail: str, status_code: int) -> Response:
        return Response(
            {"detail": detail},
            status=status_code)
