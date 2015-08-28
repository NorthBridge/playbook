from django.db import models
from . import Backlog


class AcceptanceCriteria(models.Model):
    backlog = models.ForeignKey(Backlog, db_column='backlog_id_fk')
    descr = models.CharField(max_length=500)
    title = models.CharField(max_length=80, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = "acceptance_criteria"
