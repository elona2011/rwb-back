from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .session import sessionLogin


@csrf_exempt
def deltask(request):
    data = request.POST
    taskid = data.get('taskid', '')
    userid = request.COOKIES.get('userid', '')
    if taskid != '':
        with connection.cursor() as cursor:
            cursor.execute("""
                select Appid FROM tasks WHERE id=%s and userid=%s;
                """, [taskid, userid])
            row = cursor.fetchone()
            if row != None:
                print(row[0])
                payload = {'appid': row[0], 'status': 0}
                sessionLogin.get(
                    'http://u.zrb.net/user/DelChannel', params=payload)
                with connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM tasks WHERE id=%s and userid=%s;
                        """, [taskid, userid])

    return HttpResponse(json.dumps({"code": 0}))
