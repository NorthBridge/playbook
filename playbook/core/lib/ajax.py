import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def login_required(function=None):

    # ensure the user is authenticated to access a certain ajax view
    # otherwise return a json object notifying the user access is denied
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            elif request.is_ajax():
                kwargs = {'content_type': 'application/json'}
                response = {'status': '401'}
                return HttpResponse(status=401,
                                    content=json.dumps(response),
                                    **kwargs)
            else:
                return redirect(reverse('login'))
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
