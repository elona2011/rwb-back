from django.http import HttpResponse
import json
from django.db import connection


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        session = request.COOKIES.get('session', '')
        print(session)
        with connection.cursor() as cursor:
            cursor.execute("""
                select id from users where session=%s
                """, [session])
            row = cursor.fetchone()
            if row == None and request.path != '/tasks/login':
                return HttpResponse('Unauthorized', status=401)
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
