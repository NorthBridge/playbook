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

#based on https://github.com/razius/github-webhook-handler/blob/master/index.py

@application.route("/githubimport/", methods = ['GET', 'POST'])
def index():
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger("playbook")

    # START TIME
    logger.info('IMPORT PROCESS STARTED')
    
    exit_code = 0
    
    if request.method != 'POST':
        abort(501)
    
#     verify_source(request)
    verify_secret(request)
    event = request.headers.get('X-GitHub-Event', None)
    if event == 'issues':
        try:
            payload = loads(request.data)
            import_information(payload)
        except:
            logger.exception("Error!!!!")
            abort(400)
             
    #Return information to store on github
    logger.info('IMPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)
    return '200'

def import_information(payload):
    action = payload.get('action', None)
    if action is not None:
        issue = build_issue_from_gh_payload(payload)
        milestone = build_milestone_from_gh_payload(payload)
        milestone.updateStatus(issue, action)
    else:
        logger.info("Invalid action \'%s\'", action)
    
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