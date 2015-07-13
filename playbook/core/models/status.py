from django.db import models


class Status(models.Model):
    category = models.CharField(max_length=12)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s:%s" % (self.category, self.name)

    class Meta:
        db_table = "status"
