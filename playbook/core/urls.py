from django.conf.urls import url

from views import ChooseTeam

urlpatterns = [
    url(r'^chooseTeam$', ChooseTeam.as_view(), name='chooseTeam'),
]
