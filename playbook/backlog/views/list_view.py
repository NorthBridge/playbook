from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import JsonResponse
from ...core.models import Backlog, Estimate, Event, Status
from django.views.generic import View
from ...backlog.forms.backlog_form import AcceptanceCriteriaFormSet,\
    EstimateForm, BacklogUpdateForm
from ...core.views.mixins.requiresigninajax import RequireSignInAjax
from ..github.export_to import export_to_github
from ..constants import OPEN_STATUS, SELECTED_STATUS, QUEUED_STATUS


class BacklogView(RequireSignInAjax, View):

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
            results['success'] = True
        else:
            results['errors'] = form.errors

    def select_sprint(self, request, results):
        backlog_id = request.POST.get('backlog-id')
        sprint_id = request.POST.get('backlog-sprint')
        if not backlog_id:
            results['errors'] = ("Please provide a valid Backlog.")
        elif not sprint_id:
            results['errors'] = ("Please provide a valid Sprint.")
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
            except Event.DoesNotExist:
                results['errors'] = "Sprint does not exist."
            except Backlog.DoesNotExist:
                results['errors'] = "Backlog does not exist."
            except Status.DoesNotExist:
                results['errors'] = "Status does not exist."
            except Exception as e:
                results['errors'] = str(e)
            else:
                results['status'] = backlog.status.name
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

            if form.is_valid() and formset.is_valid():
                backlog = form.save()
                formset.save()
                formset = AcceptanceCriteriaFormSet(
                    instance=backlog, prefix=prefix)
                html = render_to_string('backlog/acc_cri_par.txt',
                                        {'acceptance_criteria': formset})
                results['html'] = html
                results['mgt_fields'] = formset.management_form.as_p()
                results['success'] = True
            else:
                results['errors'] = form.errors, formset.errors
