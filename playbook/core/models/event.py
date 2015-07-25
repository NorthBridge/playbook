from django.db import models
from . import Schedule


class Event(models.Model):
    name = models.CharField(max_length=50)
    schedule = models.ForeignKey(Schedule, db_column='schedule_id_fk', null=True)
    start_dttm = models.DateField(null=True)
    end_dttm = models.DateField(null=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.start_dttm.strftime("%m/%d/%y"),
                                 self.end_dttm.strftime("%m/%d/%y"),
                                 self.name)

    class Meta:
        db_table = "event"
