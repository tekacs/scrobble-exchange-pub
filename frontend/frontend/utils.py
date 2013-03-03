from django.http import HttpResponse, HttpResponseForbidden
import json

# Import thrift stuff
import os, sys, glob
from se_api import ScrobbleExchange, ttypes
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
# End of thrift

def json_response(auth_needed = False):
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

# class APIClient:
#     API_SERVER = 'ec2-54-246-25-244.eu-west-1.compute.amazonaws.com'
#     API_PORT = 9090

#     try:
#         # Connect to the API server
#         transport = TSocket.TSocket(API_SERVER, API_PORT)
#         transport = TTransport.TBufferedTransport(transport)
#         protocol = TBinaryProtocol.TBinaryProtocol(transport)
#         CLIENT = ScrobbleExchange.Client(protocol)
#         transport.open()
#         # End

#     except Thrift.TException, tx:
#         print '%s' % (tx.message)
