from django.db import models
from . import Application
from . import Schedule
from . import Event


class Project(models.Model):
    application = models.ForeignKey(Application, db_column='application_id_fk')
    schedule = models.ForeignKey(Schedule, db_column='schedule_id_fk')
    name = models.CharField(max_length=120, null=True, default='NULL')
    descr = models.CharField(max_length=1000, null=True, default='NULL')
    start_event = models.ForeignKey(Event, db_column='start_event_fk',
                                    related_name='start')
    end_event = models.ForeignKey(Event, db_column='end_event_fk',
                                  related_name='end')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "project"
