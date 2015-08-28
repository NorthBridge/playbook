from django.conf.urls import url

from apps.shared.views import ChooseTeam

urlpatterns = [
    url(r'^chooseTeam$', ChooseTeam.as_view(), name='chooseTeam'),
]
