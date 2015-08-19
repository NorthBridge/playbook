from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import JsonResponse
from django.views.generic import View
from django.utils.timezone import localtime
from ..github.export_to import export_to_github
from ..util import open_status_id, selected_status_id, queued_status_id,\
    retrieve_backlogs_by_status_project_and_priority
from ...core.models import Backlog, Estimate, Event, Status, Team
from ...core.shortcuts import create_json_message_object
from ...backlog.forms import AcceptanceCriteriaFormSet,\
    EstimateForm, BacklogUpdateForm
from ...core.views.mixins.requiresigninajax import RequireSignIn


class BacklogView(RequireSignIn, View):

    def get(self, request):
        # Get the volunteers team
        team_id = request.session.get('team')
        # Redirects to the index page if there is no team associated
        if team_id is None:
            return redirect(reverse('index'))
        # From here now we have all we need to list the backlogs
        backlogs = retrieve_backlogs_by_status_project_and_priority(team_id)\
            .order_by('project__name', 'priority', 'module', 'id')
        backlog_tuple = []
        for backlog in backlogs:
            read_only = backlog.status.id == queued_status_id()

            try:
                estimate = Estimate.objects.get(team_id=team_id,
                                                backlog_id=backlog.id)
            except Estimate.DoesNotExist:
                estimate = Estimate()
                estimate.team_id = team_id
                estimate.backlog_id = backlog.id

            # Creates the backlog form to edit data like story descr, skills,
            # notes, etc
            form = BacklogUpdateForm(read_only=read_only, instance=backlog,
                                     prefix='backlog')
            # Creates the estimate form to edit the estimate time of the
            # specific backlog
            form_estimate = EstimateForm(instance=estimate, prefix='estimate')
            # Creates a set of forms that represents each acceptance
            # criteria linked to the specific backlog
            prefix = 'acceptance-criteria-%d' % backlog.id
            formset = AcceptanceCriteriaFormSet(instance=backlog,
                                                prefix=prefix)

            # Apeend all these information to be sent in the context
            backlog_tuple.append((backlog, form_estimate, form, formset),)

        context = RequestContext(request, {'backlogs': backlog_tuple, })
        return render(request, 'backlog/backlog_list.html', context)

    def post(self, request):
        # Get volunteers team
        team_id = request.session.get('team')
        # Redirects to the index page if there is no team associated
        if team_id is None:
            return redirect('index')

        results = {'success': False}

        if 'action-update-estimate' in request.POST:
            self.update_estimate(request, results, team_id)
        elif 'action-save' in request.POST:
            self.update_backlog_and_acc_cri(request, results)
        elif 'action-select-sprint':
            self.select_sprint(request, results)

        return JsonResponse(results)

    def update_estimate(self, request, results, team_id):
        backlog_id = request.POST.get('estimate-backlog_id')
        try:
            estimate = Estimate.objects.get(
                team_id=team_id, backlog_id=backlog_id)
        except Estimate.DoesNotExist:
            estimate = None

        form = EstimateForm(request.POST, prefix='estimate',
                            instance=estimate)

        if form.is_valid():
            form.save()
            backlog = Backlog.objects.get(id=backlog_id)
            backlog.save()
            backlog.refresh_from_db()
            results['update_dttm'] = localtime(backlog.update_dttm)
            results['success'] = True
        else:
            results['errors'] = form.errors.as_json()

    def select_sprint(self, request, results):
        backlog_id = request.POST.get('backlog-id')
        sprint_id = request.POST.get('backlog-sprint')
        if not backlog_id:
            results['errors'] = create_json_message_object(
                "Please provide a valid Backlog.")
        elif not sprint_id:
            results['errors'] = create_json_message_object(
                "Please provide a valid Sprint.")
        else:
            try:
                team_id = request.session.get('team')
                # TODO: Should we validate if the user has privileges
                #  over this backlog and sprint before updating?
                backlog = Backlog.objects.get(id=backlog_id)
                # If the volunteer trying to update the sprint is not
                #  a member of the team that first selected the backlog
                #  then he/she is not allowed to execute the update.
                if not backlog.team or team_id == backlog.team.id:
                    sprint = Event.objects.get(id=sprint_id)
                    team = Team.objects.get(id=team_id)
                    backlog.sprint = sprint
                    backlog.team = team
                    if backlog.status.id == open_status_id():
                        status = Status.objects.get(id=selected_status_id())
                        backlog.status = status
                    backlog.save()
                    export_to_github(backlog)
                    backlog.refresh_from_db()

                    results['status'] = backlog.status.name
                    if backlog.update_dttm:
                        results['update_dttm'] = localtime(backlog.update_dttm)
                    results['sprintName'] = str(sprint)
                    results['success'] = True
                else:
                    results['errors'] = create_json_message_object(
                        "This backlog was previously selected by another" +
                        " team and can only be updated by a member of" +
                        " that team.")
            except Event.DoesNotExist:
                results['errors'] = create_json_message_object(
                    "Sprint does not exist.")
            except Backlog.DoesNotExist:
                results['errors'] = create_json_message_object(
                    "Backlog does not exist.")
            except Status.DoesNotExist:
                results['errors'] = create_json_message_object(
                    "Status does not exist.")
            except Exception as e:
                results['errors'] = create_json_message_object(
                    str(e), code="exception")

    def update_backlog_and_acc_cri(self, request, results):
        backlog_id = request.POST.get('backlog-id')
        try:
            backlog = Backlog.objects.get(id=backlog_id)
        except Backlog.DoesNotExist:
            backlog = None
        else:
            form = BacklogUpdateForm(request.POST,
                                     prefix='backlog', instance=backlog)

            prefix = 'acceptance-criteria-%d' % backlog.id
            formset = AcceptanceCriteriaFormSet(request.POST,
                                                instance=backlog,
                                                prefix=prefix)
            if form.is_valid():
                if formset.is_valid():
                    backlog = form.save()
                    backlog.refresh_from_db()
                    formset.save()
                    formset = AcceptanceCriteriaFormSet(
                        instance=backlog, prefix=prefix)
                    html = render_to_string('backlog/acc_cri_par.txt',
                                            {'form': form, 'formset': formset})
                    results['html'] = html
                    results['mgt_fields'] = formset.management_form.as_p()
                    results['update_dttm'] = localtime(backlog.update_dttm)
                    results['success'] = True
                else:
                    results['errors'] = formset.non_form_errors()
            else:
                results['errors'] = form.errors.as_json()
