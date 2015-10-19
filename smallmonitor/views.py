from django.http import HttpResponse
import sys


def homepage(request):
    response = HttpResponse(open(sys.path[0] + "/api/static/pages/index.html"))
    return response


def manager(request, appid):
    return HttpResponse(open(sys.path[0] + "/api/static/pages/manager.html"))
