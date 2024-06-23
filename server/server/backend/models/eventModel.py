from django.db import models
from .calendarModel import Calendar


class Event(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start = models.TextField()
    end = models.TextField()

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
