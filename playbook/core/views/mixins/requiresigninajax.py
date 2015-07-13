from django.utils.decorators import method_decorator
from ....core.lib.ajax import login_required_ajax
from django.contrib.auth.decorators import login_required


class RequireSignInAjax(object):

    @method_decorator(login_required)
    @method_decorator(login_required_ajax())
    def dispatch(self, request, *args, **kwargs):
        return super(RequireSignInAjax, self).dispatch(
            request, *args, **kwargs)
