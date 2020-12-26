from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .session import sessionLogin


@csrf_exempt
def newtask(request):
    data = request.POST
    sitename = data.get('sitename', '')
    QICQ = data.get('QICQ', '')
    balanceName = data.get('balanceName', '')
    balanceRate = data.get('balanceRate', '')
    percentage = data.get('percentage', '')

    res = sessionLogin.get('http://u.zrb.net/user/Channel')
    print(res.content.decode('utf-8'))
    try:
        r = re.search(r'appid1">([a-z0-9]+)<', str(res.content))
        appid = r.group(1)
        r = re.search(
            r'Appkey"\smaxlength="25"\svalue="([a-z0-9]+)">', str(res.content))
        appkey = r.group(1)
        payload = {
            'apiid': (None, '对接型'),
            'sitename': (None, sitename),
            'sitelogo': (None, ''),
            'QICQ': (None, QICQ),
            'balanceName': (None, balanceName),
            'balanceRate': (None, balanceRate),
            'percentage': (None, percentage),
            'Appid': (None, appid),
            'Appkey': (None, appkey),
            'addBalanceUrl': (None, 'http://www.xlcmll.top/taskdone'),
        }
        print(payload)

        res = sessionLogin.post(
            'http://u.zrb.net/user/Channel', files=payload)
        print(res.content.decode('utf-8'))
    except Exception as identifier:
        print(identifier)
        return HttpResponse('Unauthorized', status=401)

    r = re.search(r'任务墙列表(.|\n)+任务墙地址(.|\n)+管理任务', res.content.decode("utf-8"))
    print(r)
    if r != None:
        userid = request.COOKIES.get('userid', '')
        username = request.COOKIES.get('username', '')
        if userid != '':
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tasks(userid,username,sitename,QICQ,balanceName,balanceRate,percentage,appid)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s);
                    """, [userid, username, sitename, QICQ, balanceName, balanceRate, percentage, appid])
                # print(cursor.lastrowid)
            return HttpResponse(json.dumps({"code": 0}))
    return HttpResponse(json.dumps({"code": 1}))
