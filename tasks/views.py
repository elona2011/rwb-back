from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
import threading
import time
import requests
import re

headers = {
    'Host': 'u.zrb.net',
    'Referer': 'http://u.zrb.net/user/userindex',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}


# class myThread (threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         while True:
#             print("Starting 1")
#             res = requests.get(
#                 'http://u.zrb.net/user/Channel_list', headers=headers)
#             print(res.content)
#             time.sleep(190)


# thread = myThread()
# thread.start()


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
    session = requests.Session()

    res = session.get('http://u.zrb.net/user/Channel', headers=headers)
    # print(res.content)
    try:
        r = re.search(r'appid1">([a-z0-9]+)<', str(res.content))
        appid = r.group(1)
        r = re.search(
            r'Appkey"\smaxlength="25"\svalue="([a-z0-9]+)">', str(res.content))
        appkey = r.group(1)
        payload = {
            'apiid': '人人赚',
            'sitename': 'test2',
            'QICQ': '75034320',
            'balanceName': '100',
            'percentage': '90',
            'Appid': appid,
            'Appkey': appkey
        }
        print(payload)
    except Exception as identifier:
        session2 = requests.Session()
        res = session2.get('http://u.zrb.net/gif.aspx?' +
                           uuid.uuid4().hex, headers=headers)
        print(res.content)
        with open('/code/captcha.png', 'wb') as f:
            f.write(res.content)
        return HttpResponse('Unauthorized', status=401)

    r = json.dumps({"code": 0, "result": 0})
    return HttpResponse(res.content)


@csrf_exempt
def getcaptcha(request):
    with open('/code/captcha.png', 'rb') as f:
        data = f.read()
    res = HttpResponse(data, content_type='image/png')
    return res
