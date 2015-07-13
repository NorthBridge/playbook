from django.conf.urls import url

from .views import BacklogView, GitHubWebhookView

urlpatterns = [
    url(r'^$', BacklogView.as_view(), name='backlogs'),
    url(r'^githubimport$', GitHubWebhookView.as_view(), name='ghWebhook'),
]
