from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .session import sessionLogin


@csrf_exempt
def tasklist(request):
    session = request.COOKIES.get('session', '')
    with connection.cursor() as cursor:
        cursor.execute("""
            create table IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid int NOT NULL,
                sitename TEXT NOT NULL,
                QICQ TEXT NOT NULL,
                balanceName TEXT NOT NULL,
                balanceRate TEXT NOT NULL,
                percentage TEXT NOT NULL,
                Appid TEXT NOT NULL,
                createtime datetime default current_timestamp
            )
            """)
        cursor.execute("""
            select tasks.id,tasks.sitename,tasks.QICQ,tasks.balanceRate,tasks.percentage,datetime(tasks.createtime,'localtime') as date from tasks inner join users on tasks.userid=users.id and users.session=%s
            """, [session])
        rows = cursor.fetchall()
        print(rows)
        if rows != None:
            columns = cursor.description
            data = [{columns[index][0]:column for index, column in enumerate(
                value)} for value in rows]
            return HttpResponse(json.dumps({'code': 0, 'result': data}, default=str))
    return HttpResponse(json.dumps({'code': 1}))
