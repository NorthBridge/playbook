from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ...core.models import Team
from ..forms.chooseTeamForm import ChooseTeamForm


@login_required
def index(request):

    if request.method == 'POST':
        form = ChooseTeamForm(request, request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            request.session['team'] = team
    else:
        team = request.session.get('team')

    if team is None:
        user_email = request.user.email
        try:
            teams = Team.objects.filter(volunteers__email=user_email)
        except Team.DoesNotExist:
            # TODO: Volunteer not associated with a team. What to do?
            pass
        else:
            if (len(teams) > 1):
                form = ChooseTeamForm(request)
                context = RequestContext(request, {'teams': teams,
                                                   'form': form})
                return render(request, 'core/index.html', context)
            else:
                request.session['team'] = teams[0].id
    return render(request, 'core/index.html')
