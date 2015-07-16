from django import forms
from ..models import Team


class ChooseTeamForm(forms.Form):

    team = forms.ChoiceField(choices=[], widget=forms.Select(),
                             required=True, label='Choose a Team')

    def __init__(self, request, *args, **kwargs):
        super(ChooseTeamForm, self).__init__(*args, **kwargs)
        user_email = request.user.email
        self.fields['team'].choices = Team.objects.filter(
            volunteers__email=user_email).values_list('id', 'name').distinct()
