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
        teams = Team.objects.filter(volunteers__email=user_email)
        if (len(teams) == 0):
            request.session['team'] = None
        elif (len(teams) == 1):
            request.session['team'] = teams[0].id
        else:
            form = ChooseTeamForm(request)
            context = RequestContext(request, {'teams': teams,
                                               'form': form})
            return render(request, 'core/index.html', context)
    return render(request, 'core/index.html')
