from django.http import JsonResponse
from django.views.generic import View
from django.template.loader import render_to_string
from ...core.models import Team
from ...core.shortcuts import create_json_message_object
from ...core.forms.choose_team_form import ChooseTeamForm
from ...core.views.mixins.requiresigninajax import RequireSignIn


class ChooseTeam(RequireSignIn, View):

    def get(self, request):
        results = {'success': False}
        user_email = request.user.email
        teams = Team.objects.filter(volunteers__email=user_email)
        if (len(teams) == 0):
            results['errors'] = create_json_message_object(
                "There is no team associated with this volunteer.")
        elif (len(teams) == 1):
            request.session['team'] = teams[0].id
            results['messages'] = create_json_message_object(
                "Unique team already associated")
        else:
            form = ChooseTeamForm(request)
            results['html'] = render_to_string('core/choose_team.txt',
                                               {'form': form})
            results['success'] = True
        return JsonResponse(results)

    def post(self, request):
        results = {'success': False}
        form = ChooseTeamForm(request, request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            request.session['team'] = team
            results['success'] = True
        else:
            results['errors'] = form.errors.as_json()
        return JsonResponse(results)
