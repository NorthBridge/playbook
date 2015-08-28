from django.db import models


class Estimate(models.Model):
    #models.OneToOneField(Team, 'id', db_column='team_id_fk', primary_key=True)
    #models.OneToOneField(Backlog, 'id', db_column='backlog_id_fk')
    team_id = models.IntegerField(db_column='team_id_fk')
    backlog_id = models.IntegerField(db_column='backlog_id_fk')
    estimate = models.CharField(max_length=3)

    def __unicode__(self):
        return "(%s, %s, %s)" % (self.team_id, self.backlog_id, self.estimate)

    class Meta:
        db_table = "estimate"
        unique_together = (('team_id', 'backlog_id'),)
