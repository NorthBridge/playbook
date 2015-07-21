from django.contrib import admin
from .models import Backlog, Event, Team, AcceptanceCriteria, Status

admin.site.register(Backlog)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(AcceptanceCriteria)
admin.site.register(Status)
