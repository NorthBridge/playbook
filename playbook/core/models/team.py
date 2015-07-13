from django.db import models
from . import Volunteer


class Team(models.Model):
    focus = models.CharField(max_length=50)
    name = models.CharField(max_length=250, null=True)
    visibility = models.CharField(max_length=10, default='Private')
    task_manager_id = models.IntegerField(null=True)
    volunteers = models.ManyToManyField(Volunteer, through='TeamVolunteer')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "team"
