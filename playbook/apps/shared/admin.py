from django.contrib import admin
from apps.shared.models import Backlog, Event, Team, AcceptanceCriteria, Status,\
    Application, Campaign, Estimate, Project, Schedule, TeamProject,\
    TeamVolunteer, Volunteer

admin.site.register(Backlog)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(AcceptanceCriteria)
admin.site.register(Status)
admin.site.register(Application)
admin.site.register(Campaign)
admin.site.register(Estimate)
admin.site.register(Project)
admin.site.register(Schedule)
admin.site.register(TeamProject)
admin.site.register(TeamVolunteer)
admin.site.register(Volunteer)
