import json
import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.utils.dateparse import parse_datetime
from ...core.models import Backlog
from ...core.views.mixins.requiresigninajax import RequireSignIn


class CheckBacklogsView(RequireSignIn, View):

    def post(self, request):
        result = {'outdated': False}
        team_id = request.session.get('team')
        ui_backlogs = json.loads(request.body).get("backlogs")

        if ui_backlogs and team_id:
            ui_backlogs_count = len(ui_backlogs)
            # Same query executed in the BacklogView class
            db_backlogs_count = Backlog.objects.filter(
                team__id=team_id, status__id__in=[13, 14, 15],
                priority__in=['0', '1', '2']).count()

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
                            ui_backlog.get('lastUpdated')) +\
                            datetime.timedelta(milliseconds=500)
                        db_last_update = backlog.update_dttm
                        if db_last_update > ui_last_update:
                            result['outdated'] = True
        return JsonResponse(result)
