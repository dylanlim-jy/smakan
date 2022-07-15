import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    name            = models.CharField(max_length=120, blank=False, unique=True)
    url             = models.URLField(max_length=500, blank=True)
    
    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)
    creator         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_creator')
    created_date    = models.DateTimeField(auto_now_add=True)
    voters          = models.ManyToManyField(User, blank=True, related_name='event_voters')
    note            = models.TextField(blank=True)
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_date <= now

    def get_voters(self):
        return [v.username for v in self.voters.all()]

    def __str__(self) -> str:
        return str(self.created_date)