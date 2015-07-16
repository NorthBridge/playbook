import json
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import JsonResponse
from django.views.generic import View
from django.utils.timezone import localtime
from ...core.models import Backlog, Estimate, Event, Status
from ...backlog.forms.backlog_form import AcceptanceCriteriaFormSet,\
    EstimateForm, BacklogUpdateForm
from ...core.views.mixins.requiresigninajax import RequireSignIn
from ..github.export_to import export_to_github
from ..constants import OPEN_STATUS, SELECTED_STATUS, QUEUED_STATUS


class BacklogView(RequireSignIn, View):

    def get(self, request):
        # Get the volunteers team
        team_id = request.session.get('team')
        # Redirects to the index page if there is no team associated
        if team_id is None:
            return redirect(reverse('index'))

        # From here now we have all we need to list the backlogs
        backlogs = Backlog.objects.filter(team__id=team_id,
                                          status__id__in=[13, 14, 15],
                                          priority__in=['0', '1', '2'])\
            .order_by('project__name', 'priority', 'module', 'id')

        backlog_tuple = []
        for backlog in backlogs:
            read_only = backlog.status.id == QUEUED_STATUS

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
            results['errors'] = self.create_error_json_object(
                "Please provide a valid Backlog.")
        elif not sprint_id:
            results['errors'] = self.create_error_json_object(
                "Please provide a valid Sprint.")
        else:
            try:
                # TODO: Should we validate if the user has privileges
                #  over this backlog and sprint before updating?
                backlog = Backlog.objects.get(id=backlog_id)
                sprint = Event.objects.get(id=sprint_id)
                backlog.sprint = sprint
                if backlog.status.id == OPEN_STATUS:
                    status = Status.objects.get(id=SELECTED_STATUS)
                    backlog.status = status
                backlog.save()
                export_to_github(backlog)
                backlog.refresh_from_db()
            except Event.DoesNotExist:
                results['errors'] = self.create_error_json_object(
                    "Sprint does not exist.")
            except Backlog.DoesNotExist:
                results['errors'] = self.create_error_json_object(
                    "Backlog does not exist.")
            except Status.DoesNotExist:
                results['errors'] = self.create_error_json_object(
                    "Status does not exist.")
            except Exception as e:
                results['errors'] = self.create_error_json_object(
                    str(e), "exception")
            else:
                results['status'] = backlog.status.name
                results['update_dttm'] = localtime(backlog.update_dttm)
                results['sprintName'] = str(sprint)
                results['success'] = True

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

    def create_error_json_object(self, message, code="invalid"):
        return json.dumps({"__all__": [{"message": message, "code": code}]})
