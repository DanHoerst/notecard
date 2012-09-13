import django.db
from notecard.notecards.models import *

class NotecardKeyword(django.db.models.Model):
    keyword = django.db.models.CharField(max_length=50)
    page = django.db.models.ForeignKey(Notecard)

    def __unicode__(self):
        return self.keyword
