from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=25, null=True, default='NULL')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "schedule"
