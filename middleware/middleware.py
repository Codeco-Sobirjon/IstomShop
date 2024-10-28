from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404

class JsonErrorResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error_message = str(exception)
        response_data = {"error": error_message}
        return JsonResponse(response_data, status=500)


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response is None:
            return self.handle_404(request)

        if response.status_code == status.HTTP_404_NOT_FOUND:
            return self.handle_404(request)

        return response

    def handle_404(self, request):
        data = {'detail': 'Page Not found'}
        return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
