from django.conf.urls import url

from .views import BacklogView, GitHubWebhookView, CheckBacklogsView

urlpatterns = [
    url(r'^$', BacklogView.as_view(), name='backlogs'),
    url(r'^checkBacklogs$', CheckBacklogsView.as_view(),
        name='checkBacklogsUpdate'),
    url(r'^githubimport$', GitHubWebhookView.as_view(), name='ghWebhook'),
]
