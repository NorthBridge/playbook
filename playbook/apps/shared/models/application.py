from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=200, null=True, default='NULL')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "application"
