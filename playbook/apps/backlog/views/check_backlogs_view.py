import json
import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.utils.dateparse import parse_datetime
from ..util import retrieve_backlogs_by_status_project_and_priority
from apps.shared.models import Backlog
from apps.shared.views.mixins.requiresigninajax import RequireSignIn


class CheckBacklogsView(RequireSignIn, View):

    def post(self, request):
        result = {'outdated': False}
        team_id = request.session.get('team')
        ui_backlogs = json.loads(request.body).get("backlogs")

        if ui_backlogs and team_id:
            ui_backlogs_count = len(ui_backlogs)
            # Same query executed in the BacklogView class
            db_backlogs_count = \
                retrieve_backlogs_by_status_project_and_priority(team_id)\
                .count()

            # If the number of backlogs displayed to the user
            #  differs from the number that exists into database
            #  then user must refresh his/her page.
            if (ui_backlogs_count != db_backlogs_count):
                result['outdated'] = True
            else:
                # Otherwise we must compare the last update time
                #  of each backlog displayed to the user with those
                #  existing into database.
                for ui_backlog in ui_backlogs:
                    backlog_id = ui_backlog.get('id')
                    try:
                        backlog = Backlog.objects.get(id=backlog_id)
                    except Backlog.DoesNotExist:
                        # Maybe this backlog has been deleted by an
                        #  admin user.
                        result['outdated'] = True
                    else:
                        # Database datetime has greater precision than
                        #  the one brought from ui so we add a timedelta,
                        #  otherwise the page that executed the update
                        #  would show the message of requested refresh.
                        ui_last_update = parse_datetime(
                            ui_backlog.get('lastUpdated'))
                        db_last_update = backlog.update_dttm

                        if not ui_last_update and db_last_update:
                            result['outdated'] = True
                        elif db_last_update:
                            ui_last_update += datetime.timedelta(
                                milliseconds=500)
                            if db_last_update > ui_last_update:
                                result['outdated'] = True
        return JsonResponse(result)
