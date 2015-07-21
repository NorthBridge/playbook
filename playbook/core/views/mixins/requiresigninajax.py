from django.utils.decorators import method_decorator
from ....core.lib.ajax import login_required


class RequireSignIn(object):

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(RequireSignIn, self).dispatch(
            request, *args, **kwargs)
