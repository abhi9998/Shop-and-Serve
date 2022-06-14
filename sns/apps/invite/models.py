from django.db import models
from sns.apps.user.models import Group
from django.conf import settings


# Create your models here.
class Invite(models.Model):
    class Meta:
        db_table = "invite"

    createAt = models.DateTimeField(auto_now=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    groupid = models.ForeignKey(Group, to_field='id', on_delete=models.CASCADE)
