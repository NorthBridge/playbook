import json
import logging
import traceback
from pygithub3 import Github
from ..github import create_milestone_data
from ..constants import ACCEPT_ISSUE_LABEL, GH_ACTION
from ..github_settings import GITHUB_OWNER, GITHUB_TOKEN
from ...core.shortcuts import send_email
from ...core.models import Backlog, Status

logger = logging.getLogger("playbook")


def import_from_github(payload):
    action = payload.get('action', None)
    if action:
        message = None
        issue_title = payload['issue']['title']
        issue_labels = payload['issue']['labels']

        if __is_acceptance_issue(issue_labels):
            gh_number = payload['issue']['milestone']['number']
            try:
                backlog = Backlog.objects.get(github_number=gh_number)
            except Backlog.DoesNotExist:
                message = ("There is no backlog associated with this"
                           " github number (number=%s)") % gh_number
                logger.info(message)
                __notify_import_problem(message, payload,
                                        traceback.format_exc())
            else:
                new_milestone_state = None
                new_milestone_status = None

                try:
                    new_milestone_state = GH_ACTION[action]['gh_state']
                    new_milestone_status = GH_ACTION[action]['db_status']

                    __update_db(backlog, new_milestone_status)
                    __update_gh(backlog, new_milestone_state)

                    message = ("Milestone #%s from \'%s\' repo updated to"
                               " status \'%s\' using issue \'%s\'") %\
                        (backlog.github_number, backlog.github_repo,
                         new_milestone_state, issue_title)
                except KeyError:
                    message = ("Invalid action passed as argument: \'%s\'." +
                               " This request is being ignored..." % action)
                    logger.error(message)
                except Exception:
                    message = ("Error updating milestone #%s from \'%s\'" +
                               " repo using issue \'%s\'") %\
                        (backlog.github_number, backlog.github_repo,
                         issue_title)
                    logger.exception(message)
                    __notify_import_problem(message, payload,
                                            traceback.format_exc())
                    raise
        else:
            message = ("Issues without \"owner acceptance\" label are not" +
                       " treated.")
        return message
    else:
        message = "\'action\' not defined in payload. Ignoring request..."
        logger.error(message)
        __notify_import_problem(message, payload, traceback.format_exc())
        raise RuntimeError(message)


def __notify_import_problem(message, payload, traceback):
    subject = '[playbook.backlog] Milestone importing error'
    body = "%s\n\nPayload received:\n%s\n\n%s" %\
        (message, json.dumps(payload, indent=4), traceback)
    send_email(subject, body)


def __is_acceptance_issue(labels):
    return any(label['name'] == ACCEPT_ISSUE_LABEL
               for label in labels)


def __update_db(backlog, status_id):
    new_status = Status.objects.get(id=status_id)
    backlog.status = new_status
    backlog.save()


def __update_gh(backlog, new_state):
    github = Github(token=GITHUB_TOKEN, user=GITHUB_OWNER,
                    repo=backlog.github_repo)
    data = create_milestone_data(backlog, new_state)
    github.issues.milestones.update(backlog.github_number, data)
