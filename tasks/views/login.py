from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseNotFound
import uuid
import requests
from .session import sessionLogin
import re
from django.db import connection

isZRBLogin = False


@csrf_exempt
def isLogin(request):
    name = request.COOKIES.get('name', '')
    r = json.dumps({"code": 0, "result": name})
    return HttpResponse(r)


@csrf_exempt
def login(request):
    global token, isZRBLogin

    data = request.POST
    name = data.get('name', '')
    password = data.get('password', '')
    print(isZRBLogin)
    if isZRBLogin == False:
        captcha = data.get('captcha', '')
        payload = {
            '__RequestVerificationToken': token,
            'username': '75034320@qq.com',
            'oldPwd': 'zrb73@A',
            'userVer': captcha,
        }
        res = sessionLogin.post('http://u.zrb.net/User/Login', data=payload)
        content = res.content.decode("utf-8")
        print(content)
        r = re.search(r'验证码错误', content)
        if r != None:
            return HttpResponse('验证码错误', status=401)
        r = re.search(r'当前余额', content)
        if r != None:
            isZRBLogin = True

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
            res.set_cookie(key='name', value=name, max_age=60*60*24*300)
            return res
    return HttpResponse('密码错误', status=401)


@csrf_exempt
def getcaptcha(request):
    global token, isZRBLogin
    res = sessionLogin.get('http://u.zrb.net/User/Login')
    r = re.search(
        r'__RequestVerificationToken"\stype="hidden"\svalue="([a-zA-Z0-9\-_]+)"', str(res.content))
    if r == None:
        isZRBLogin = True
        return HttpResponseNotFound('')
    else:
        isZRBLogin = False
        token = r.group(1)
        res = sessionLogin.get('http://u.zrb.net/gif.aspx?' + uuid.uuid4().hex)
        return HttpResponse(res.content, content_type='image/png')


@csrf_exempt
def refreshcaptcha(request):
    res = sessionLogin.get('http://u.zrb.net/gif.aspx?' + uuid.uuid4().hex)
    return HttpResponse(res.content, content_type='image/png')
