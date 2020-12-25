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
        name = request.COOKIES.get('name', '')
        print(session)
        if request.path != '/tasks/login' and request.path != '/tasks/getcaptcha':
            with connection.cursor() as cursor:
                cursor.execute("""
                    select id from users where session=%s and name=%s
                    """, [session, name])
                row = cursor.fetchone()
                if row == None:
                    return HttpResponse('Unauthorized', status=401)
                # print(row[0])
                request.COOKIES['id'] = row[0]
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
