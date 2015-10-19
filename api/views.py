from rest_framework.decorators import api_view
from api.serializers import GroupSerializer, AppSerializer, host_serializer,\
    app_history_serializer, app_statistics_serializer, manager_app_serializer
from api.models import Group, App, Host, AppStatistics, AppHistory
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from api.lib.utils import object_to_json, RepresentsInt, api
from ipware.ip import get_ip
from datetime import datetime
import json
from api.lib.constant import MonitoringStatus


@api_view(['GET', 'POST'])
@csrf_exempt
def group_list(request):
    """
    List all gourps, or create a new group.
    """
    if request.method == 'GET':
        tasks = Group.objects.all()
        serializer = GroupSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        unique_name = request.data.get("unique_name")
        display_name = request.data.get("display_name")
        if unique_name and display_name:
            checkgoup = Group.objects.filter(unique_name=unique_name).first()
            if checkgoup:
                res = {"code": 400,
                       "message": "Ops!, Unique name already exists"}
                return Response(data=res,
                                status=400)
        else:
            res = {"code": 400,
                   "message":
                   "Ops!, Unique name and display name can't be null"}
            return Response(data=res,
                            status=400)
        group = Group.create(unique_name, display_name)
        group.save()
        serializer = GroupSerializer(group, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT'])
def group_detail(request, pk):
    """
    Get, udpate, or delete a specific task
    """
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        group.unique_name = request.data.get("unique_name", group.unique_name)
        group.display_name = request.data.get("display_name",
                                              group.display_name)
        group.save()
        return JsonResponse(object_to_json(group))


@api_view(['GET', 'POST'])
@csrf_exempt
def app_list(request):

    if request.method == 'GET':
        groupid = request.GET.get('groupid', None)
        if groupid:
            tasks = App.objects.filter(enable=1).filter(group_id=groupid).all()
        else:
            tasks = App.objects.filter(enable=1).all()
        serializer = AppSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get("name", None)
        app = App.create(name, 1, "OK", "", 1, 2).save()
        serializer = AppSerializer(app, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def app_detail(request, pk):
    try:
        try:
            pk = int(pk)
            app = App.objects.get(pk=pk)
        except:
            app = App.objects.filter(name=pk).first()
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AppSerializer(app)
        return JsonResponse(serializer.data)

    if request.method == 'DELETE':
        app.enable = 0
        app.save()
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        if not app:
            res = {"code": 405, "message": "Not found this app"}
            return Response(data=res,
                            status=405)
    ip = get_ip(request, right_most_proxy=True)
    if ip is not None:
        host = Host.objects.filter(ip=ip).first()
        if host is None:
            host = Host.create(ip)
            host.save()
    status = request.data.get("status")
    statistics = request.data.get('statistics')
    app.message = request.data.get("message", app.message)
    if status is None:
        res = {"code": 400,
               "message": "wong"}
        return Response(data=res,  status=400)
    app.status = status
    app.last_update = datetime.now()
    app.host_id = host.id
    app.save()
    if statistics:
        try:
            json.loads(statistics)
        except:
            res = {"code": 400, "message": "Statistics format must json"}
            return Response(data=res,
                            status=400)
        appStatistics = AppStatistics.create(statistics, app.id)
        appStatistics.save()
    return JsonResponse(object_to_json(app))


@api_view(['GET', 'POST'])
@csrf_exempt
def manager_detail(request, pk):
    try:
        pk = int(pk)
        app = App.objects.get(pk=pk)
    except:
        app = App.objects.filter(unique_name=pk).first()
    if not app:
        return HttpResponse(status=404)
    elif request.method == 'GET':
        serializer = manager_app_serializer(app)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        app.name = request.data.get("name", app.name)
        app.host_id = request.data.get("host_id", app.host_id)
        app.group_id = request.data.get("group_id", app.group_id)
        app.configuration = request.data.get("configuration", app.configuration)
        app.save()
        serializer = manager_app_serializer(app, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def host_list(request):
    """List all code hosts
    :rtype: json
    """
    hosts = Host.objects.all()
    serializer = host_serializer(hosts, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET', 'PUT'])
def host_detail(request, pk):
    """
    Retrieve, update or delete a code host.
    """
    try:
        host = Host.objects.get(pk=pk)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = host_serializer(host)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        host.name = request.data.get("name", host.name)
        host.description = request.data.get("description", host.description)
        host.save()
        return JsonResponse(object_to_json(host))


@api_view(['GET'])
def app_history_list(request):
    if request.method == 'GET':
        limit = request.GET.get('limit', 12)
        appid = request.GET.get('appid')
        if not RepresentsInt(limit):
            res = {"code": 404, "message": "Limit must be int"}
            return Response(data=res,
                            status=400)
        else:
            limit = int(limit)
        if not RepresentsInt(appid):
            res = {"code": 400, "message": "Appid must be int"}
            return Response(data=res,
                            status=400)
        apphistory_list = AppHistory.objects.filter(app_id=appid).order_by('-id')[:limit]
        serializer = app_history_serializer(apphistory_list, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def app_statistics_list(request, pk):
    limit = int(request.GET.get('limit', 12))
    start_date = request.GET.get('startDate', None)
    end_date = request.GET.get('endDate', None)
    if start_date and end_date:
        appstatistics_list = AppStatistics.objects.filter(app_id=pk).filter(time__range=(start_date, end_date)).order_by('-id').all()
    else:
        appstatistics_list = AppStatistics.objects.filter(app_id=pk).order_by('-id')[:limit].all()
    serializer = app_statistics_serializer(appstatistics_list, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@api
def count_groups_statistics_detail(request):
    grouplist = Group.objects.all().filter()
    group_message = []
    for group in grouplist:
        group_apps = App.objects.filter(group_id=group.id).filter(enable=1).all()
        ok_num = 0
        warn_num = 0
        critical_num = 0
        for app in group_apps:
            if app.status == MonitoringStatus.OK:
                ok_num += 1
            elif app.status == MonitoringStatus.WARN:
                warn_num += 1
            elif app.status == MonitoringStatus.CRITICAL:
                critical_num += 1
        group_app = {"id": group.id,
                     "uniqueName": group.unique_name,
                     "displayName": group.display_name,
                     "statistics": {"total": len(group_apps),
                                    MonitoringStatus.OK.lower(): ok_num,
                                    MonitoringStatus.CRITICAL.lower(): critical_num,
                                    MonitoringStatus.WARN.lower(): warn_num,
                                    }
                     }
        group_message.append(group_app)
    return group_message


@api_view(['GET'])
@api
def count_group_statistics_detail(request, pk):
    group = Group.objects.filter(id=pk).first()
    if group is None:
        res = {"code": 400, "message": "Ops!, Don't find group by this id"}
        return Response(data=res,
                        status=400)
    group_apps = App.objects.filter(group_id=group.id).filter(enable=1).all()
    ok_num = 0
    warn_num = 0
    critical_num = 0
    for app in group_apps:
        if app.status == MonitoringStatus.OK:
            ok_num += 1
        elif app.status == MonitoringStatus.WARN:
            warn_num += 1
        elif app.status == MonitoringStatus.CRITICAL:
            critical_num += 1
    group_app = {"id": group.id,
                 "uniqueName": group.unique_name,
                 "displayName": group.display_name,
                 "statistics": {"total": len(group_apps),
                                MonitoringStatus.OK.lower(): ok_num,
                                MonitoringStatus.CRITICAL.lower(): critical_num,
                                MonitoringStatus.WARN.lower(): warn_num,
                                }
                 }
    return group_app
