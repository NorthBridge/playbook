from django.db import models
from datetime import datetime
from . import Campaign
from . import Status


class Volunteer(models.Model):
    #As auth_user.email is not unique, we cannot create a fk here.
    #email = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='email')
    email = models.CharField(max_length=255, default='NULL')
    fname = models.CharField(max_length=50, default='NULL')
    lname = models.CharField(max_length=50, null=True)
    status_depr = models.CharField(max_length=10, null=True)
    campaign = models.ForeignKey(Campaign, db_column='campaign_id_fk')
    create_dttm = models.DateTimeField(default=datetime.now)
    update_dttm = models.DateTimeField(null=True)
    descr = models.CharField(max_length=1000)
    status = models.ForeignKey(Status, db_column='status_id_fk')

    def __unicode__(self):
        return self.lname

    class Meta:
        db_table = "volunteer"
