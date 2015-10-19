
import json
from django.http import HttpResponse
import datetime
import jsonpickle
from django.db.models.query import QuerySet
import functools
import traceback
from api.lib.constant import STRFTIME_FORMAT


def api(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        try:
            response_data = jsonpickle.encode(func(*args, **kw))
        except:
            response_data = jsonpickle.encode(dict(error=traceback.print_stack))
        response = HttpResponse(response_data,
                                content_type="application/json")
        return response
    return _wrapper


def object_to_json(model, ignore=None):
    """ Returns a JSON representation of an object.
    """
    if ignore is None:
        ignore = []
    if type(model) in [QuerySet, list]:
        json = []
        for element in model:
            json.append(_django_single_object_to_json(element, ignore))
        return json
    else:
        return _django_single_object_to_json(model, ignore)


def _django_single_object_to_json(element, ignore=None):
    json = {}
    for col in element._meta.get_all_field_names():
        if col not in ignore:
            value = getattr(element, col)
            if (type(value) is datetime.datetime) or (type(value) is datetime.date):
                value = value.strftime(STRFTIME_FORMAT)
            json[col] = value
    return json


def verification_string_is_json(string):
    try:
        json.loads(string)
        return True
    except:
        return False


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
