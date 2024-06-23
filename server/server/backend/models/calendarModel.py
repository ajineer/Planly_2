from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .userModel import User


class CalendarManager:
    def get_calendars(self, name, description, user):
        if not user.is_authenticated:
            raise PermissionDenied("Unauathorized")
        calendar = self.create(name=name, description=description, user=user)
        return calendar


class Calendar(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
