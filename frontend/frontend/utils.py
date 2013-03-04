from django.http import HttpResponse, HttpResponseForbidden
import json


def json_response(auth_needed=False):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            if auth_needed and not request.user.is_authenticated():
                return HttpResponseForbidden()

            objects = func(request, *args, **kwargs)
            if isinstance(objects, HttpResponse):
                return objects
            try:
                data = json.dumps(objects)
                if 'callback' in request.REQUEST:
                    # a jsonp response!
                    data = '%s(%s);' % (request.REQUEST['callback'], data)
                    return HttpResponse(data, "text/javascript")
            except:
                data = json.dumps(str(objects))
            return HttpResponse(data, "application/json")
        return inner
    return decorator


def get_current_path(request):
    return {'current_path': request.get_full_path()}
