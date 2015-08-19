import hmac
import requests
import logging.config
from json import loads
from hashlib import sha1
from ipaddress import ip_address, ip_network
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
try:
    from ..github_settings import GITHUB_WEBHOOK_SECRET
except ImportError:
    GITHUB_WEBHOOK_SECRET = None
from ..github.import_from import import_from_github


logger = logging.getLogger("playbook")


class GitHubWebhookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GitHubWebhookView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return HttpResponse("GET Method is not allowed", status=405)

    def post(self, request):
        # self.verify_source(request)
        signature_ver = self.verify_signature(request)
        if not signature_ver:
            event = request.META.get(self.meta_key_formatter('X-GitHub-Event'))
            response = None
            if event == 'issues':
                try:
                    payload = loads(request.body)
                    response = import_from_github(payload)
                except Exception, error:
                    response = repr(error)
                    logger.exception(response)
            else:
                response = 'Untreatable event: \'%s\'' % event
            return HttpResponse(response)
        else:
            return signature_ver

    # This method will return None if the signature verification
    #  run well. The other possibilities are an HttpResponse with
    #  status code = 501 if the hash algorithm is not suported or
    #  an exception raised in case of the signature does not match
    #  (in this case, Django will return an HttpResponse with status
    #  code = 403).
    def verify_signature(self, request):
        if GITHUB_WEBHOOK_SECRET:
            try:
                sha_name, signature = request.META.get(
                    self.meta_key_formatter('X-Hub-Signature')).split('=')
            except:
                # Exception will occur in case X-Hub-Signature does not
                #  exist in the request header. As GitHub always send this
                #  key, we can throw an PermissonDenied exception.
                raise PermissionDenied
            else:
                if sha_name != 'sha1':
                    logger.error("Only sha1 hash algorithm is available." +
                                 " Ignoring request...")
                    return HttpResponse("Only sha1 hash algorithm is" +
                                        " accepted.", status=501)

                mac = hmac.new(GITHUB_WEBHOOK_SECRET, request.body,
                               digestmod=sha1)
                if not hmac.compare_digest(str(mac.hexdigest()),
                                           str(signature)):
                    logger.warning("X-Hub-Signature does not match. Ignoring" +
                                   " request...")
                    raise PermissionDenied
        else:
            logger.warning("There is no secret configured in the github_settings" +
                           " file. Payload verification will not be performed." +
                           " Please add the key GITHUB_WEBHOOK_SECRET to" +
                           " the file to increase security.")
        return None

    def verify_source(self, request):
        src_ip = ip_address(u'{0}'.format(request.remote_addr))
        whitelist = requests.get('https://api.github.com/meta').json()['hooks']
        for valid_ip in whitelist:
            if src_ip in ip_network(valid_ip):
                break
        else:
            logger.warning("This request came from an server other than the" +
                           " GitHub servers. IP: %s", src_ip)
            raise PermissionDenied

    # With the exception of CONTENT_LENGTH and CONTENT_TYPE, any HTTP headers
    #  in the request are converted to META keys by converting all characters
    #  to uppercase, replacing any hyphens with underscores and adding an
    #  HTTP_ prefix to the name. So, for example, a header called X-Bender
    #  would be mapped to the META key HTTP_X_BENDER.
    # source: https://docs.djangoproject.com/en/1.8/ref/request-response
    #  /#django.http.HttpRequest.META
    def meta_key_formatter(self, key):
        return 'HTTP_' + key.replace("-", "_").upper()
