from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .session import sessionLogin


@csrf_exempt
def taskdone(request):
    data = request.POST
    print('taskdone')


    return HttpResponse(json.dumps({"code": 0}))
