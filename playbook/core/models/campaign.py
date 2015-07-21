from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, default='NULL')
    amount_goal = models.DecimalField(max_digits=10, decimal_places=2)
    respondent_goal = models.CharField(max_length=10, default='NULL')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "campaign"
