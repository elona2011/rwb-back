from django.http import HttpResponse
import json


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        session = request.COOKIES.get('session', '')
        print(session)
        if session == '' and request.path != '/tasks/login':
            return HttpResponse(json.dumps({
                'code': 1
            }))
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
