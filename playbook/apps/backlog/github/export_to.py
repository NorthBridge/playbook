import logging
import traceback
from pygithub3 import Github
from ..util import queued_status_id, selected_status_id
from ..constants import ACCEPT_ISSUE_LABEL
from ..github_settings import GITHUB_OWNER, GITHUB_TOKEN
from ..github import create_milestone_data
from ...core.models.backlog import Backlog, Status
from ...core.models.acceptance_criteria import AcceptanceCriteria
from ...core.shortcuts import send_email

logger = logging.getLogger("playbook")

STATIC_LABEL_VALUE = 'acceptance criteria'
ACCEPT_ISSUE_TITLE = 'Accept the story (milestone)'


def export_to_github(backlog):
    __validate(backlog)

    github = Github(token=GITHUB_TOKEN, user=GITHUB_OWNER,
                    repo=backlog.github_repo)

    if backlog.status.id == selected_status_id():
        try:
            __export_milestone(backlog, github)
        except:
            message = ("Error exporting milestone to GitHub" +
                       " (Repo name: %s, backlog id: %d).") %\
                      (backlog.github_repo, backlog.id)
            logger.exception(message)
            __notify_export_problem(message, traceback.format_exc())
            raise
        else:
            try:
                __export_issues(backlog, github)
            except:
                message = ("Error exporting issues to GitHub" +
                           " (Repo name: %s, Milestone #: %s).") %\
                          (backlog.github_repo,
                           backlog.github_number)
                logger.exception(message)
                __rollback_status(backlog)
                __notify_export_problem(message, traceback.format_exc())
                raise

            try:
                __export_acceptance_issue(backlog, github)
            except:
                message = ("Error exporting accept issue to GitHub" +
                           " (Repo name: %s, Milestone #: %s).") %\
                          (backlog.github_repo,
                           backlog.github_number)
                logger.exception(message)
                __notify_export_problem(backlog, traceback.format_exc())
                raise
    else:
        try:
            __update_milestone(backlog, github)
        except:
            message = "Error updating milestone in GitHub."
            __notify_export_problem(message, traceback.format_exc(), True)
            logger.exception(message)
            raise


def __notify_export_problem(message, traceback=None, is_update=False):
    subject = '[playbook.backlog] Milestone exporting error'
    body = "%s\n\n%s" % (message, traceback)
    send_email(subject, body)


def __rollback_status(backlog):
    status = Status.objects.get(id=selected_status_id())
    backlog.status = status
    backlog.save()


def __create_issue_data(acceptance_criterion):
    data = {'title': acceptance_criterion.title}
    data['body'] = acceptance_criterion.descr
    data['milestone'] = acceptance_criterion.backlog.github_number
    data['labels'] = [STATIC_LABEL_VALUE,
                      acceptance_criterion.backlog.team.name]
    data['repo'] = acceptance_criterion.backlog.github_repo
    return data


def __create_acceptance_issue_data(github_number, github_repo):
    descr = ('The product owner should complete this task after all the '
             'acceptance criteria are met for this story (milestone).')
    data = {'title': ACCEPT_ISSUE_TITLE}
    data['body'] = descr
    data['milestone'] = github_number
    data['labels'] = [ACCEPT_ISSUE_LABEL]
    data['repo'] = github_repo
    return data


def __export_milestone(backlog, github):
    data = create_milestone_data(backlog)
    try:
        ghMilestone = github.issues.milestones.create(data)
    except:
        raise
    else:
        logger.info("Milestone exported to GitHub: %s", data)
        status = Status.objects.get(id=queued_status_id())
        backlog.github_number = str(ghMilestone.number)
        backlog.status = status
        backlog.save()
        logger.info("Backlog table [id=%d] updated with status = %d and" +
                    " github_number = %s",
                    backlog.id,
                    backlog.status.id,
                    backlog.github_number)


def __update_milestone(backlog, github):
    data = create_milestone_data(backlog)
    github.issues.milestones.update(backlog.github_number, data)
    logger.info("Milestone #%s from repo %s successfully updated.",
                backlog.github_number,
                backlog.github_repo)


def __export_issues(backlog, github):
    logger.info("Creating associated issues:")
    acceptance_criteria = AcceptanceCriteria.objects.\
        filter(backlog=backlog)
    for criterion in acceptance_criteria:
        data = __create_issue_data(criterion)
        github.issues.create(data)
        logger.info("Issue exported to GitHub: %s", data)


def __export_acceptance_issue(backlog, github):
    data = __create_acceptance_issue_data(backlog.github_number,
                                          backlog.github_repo)
    logger.info("Creating Accept Issue related to milestone #%s" +
                " into repository %s", backlog.github_number,
                backlog.github_repo)
    github.issues.create(data)


def __validate(backlog):
    if not isinstance(backlog, Backlog):
        errMsg = "The given object is not an instance of Backlog."
        logger.error(errMsg)
        raise Exception(errMsg)
