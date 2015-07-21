from django.db import models
from . import Team, Project, Event


class TeamProject(models.Model):
    # team_id_fk = models.IntegerField()
    # project_id_fk = models.IntegerField()
    # start_event_fk = models.IntegerField(blank=True, null=True)
    # end_event_fk = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey(Team, db_column='team_id_fk')
    project = models.ForeignKey(Project, db_column='project_id_fk')
    start_event = models.ForeignKey(Event, db_column='start_event_fk',
                                    related_name='start_event')
    end_event = models.ForeignKey(Event, db_column='end_event_fk',
                                  related_name='end_event')
    claim_backlog = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.team, self.project

    class Meta:
        db_table = 'team_project'
