from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import uuid
import json


@csrf_exempt
def login(request):
    data = request.POST
    name = data.get('name', '')
    password = data.get('password', '')
    with connection.cursor() as cursor:
        cursor.execute("""
            create table IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                createtime datetime default current_timestamp,
                lasttime datetime default current_timestamp,
                loginNum int default 1,
                session TEXT default NULL
            )
            """)
        cursor.execute("""
            select id from users where name=%s and password=%s
            """, [name, password])
        row = cursor.fetchone()
        if row != None:
            res = HttpResponse('Success', status=200)
            session = uuid.uuid4().hex
            cursor.execute("""
                UPDATE users SET session = '{session}' WHERE id = {id}; 
            """.format(session=session, id=row[0]))
            res.set_cookie(key='session', value=session, max_age=60*60*24*300)
            return res
    return HttpResponse('Unauthorized', status=401)


@csrf_exempt
def newtask(request):
    r = json.dumps({"code": 0, "result": 0})
    return HttpResponse(r)
