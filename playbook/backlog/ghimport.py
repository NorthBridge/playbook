#!/usr/bin/env python

from ..backlog import application
from flask import request, abort
from ipaddress import ip_address, ip_network
from ..utils.configHelper import getConfig
import hmac
from hashlib import sha1
from json import loads, dumps
import requests
from .model.issue import build_issue_from_gh_payload
from .model.milestone import build_milestone_from_gh_payload, Milestone
from twisted.web.xmlrpc import payloadTemplate
import logging.config

#based on:
# https://github.com/razius/github-webhook-handler/blob/master/index.py
# https://github.com/carlos-jenkins/python-github-webhooks/blob/master/webhooks.py

@application.route("/githubimport/", methods = ['POST'])
def index():
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger("playbook")
    exit_code = 0
    
    # START TIME
    logger.info('IMPORT PROCESS STARTED')

#     verify_source(request)
    verify_secret(request)
    event = request.headers.get('X-GitHub-Event', None)
    response = None
    if event == 'issues':
        try:
            payload = loads(request.data)
            response = import_information(payload)
        except Exception, error:
            response = repr(error)
    else:
        response = 'Untreatable event: \'%s\'' % event
    logger.info('IMPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)
    return response

def import_information(payload):
    action = payload.get('action', None)
    if action is not None:
        issue = build_issue_from_gh_payload(payload)
        milestone = build_milestone_from_gh_payload(payload)
        return milestone.updateStatus(issue, action)
    else:
        raise RuntimeError("action not defined in payload. Ignoring request...")
    
def verify_secret(request):
    secret = getConfig('github.webhooks.secret')
    if secret:
        sha_name, signature = request.headers.get('X-Hub-Signature').split('=')
        if sha_name != 'sha1':
            abort(501)

        # HMAC requires the key to be bytes, but data is string
        mac = hmac.new(str(secret), msg=request.data, digestmod=sha1)
        if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
            abort(403)
    
def verify_source(request):
    src_ip = ip_address(u'{0}'.format(request.remote_addr))
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']
    for valid_ip in whitelist:
        if src_ip in ip_network(valid_ip):
            break
    else:
        abort(403)
        
def start_server():
    application.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__':
    start_server()
    