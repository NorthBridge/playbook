from django.db import models


class Status(models.Model):
    category = models.CharField(max_length=12)
    name = models.CharField(max_length=20)
    descr = models.CharField(max_length=20, default=None)

    def __unicode__(self):
        return "%s" % self.descr

    class Meta:
        db_table = "status"
        unique_together = (('category', 'name'),)
