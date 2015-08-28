from django.db import models
from . import Volunteer
from . import Team


class TeamVolunteer(models.Model):
    volunteer = models.ForeignKey(Volunteer, db_column='volunteer_id_fk')
    team = models.ForeignKey(Team, db_column='team_id_fk')
    role = models.CharField(max_length=20, default='Follower')
    conference_link = models.CharField(max_length=120, default='NULL')

    class Meta:
        db_table = "team_volunteer"
        unique_together = ('volunteer', 'team')
