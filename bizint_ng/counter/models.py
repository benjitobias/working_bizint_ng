from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Action(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('Date created', default=timezone.now) # Not to call funtion, server will call on run

    def get_count(self):
        try:
            count_id = self.count_set.last().id
            count_object = self.count_set.get(id=count_id)
            count = count_object.count
        except AttributeError:
            count = 0
        return count

    def get_latest(self):
        try:
            latest = self.count_set.last()
        except AttributeError:
            latest = None
        return latest

    def __str__(self):
        return self.name


class Count(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    # Don't call timezone.now function, server will call on run
    update_date = models.DateTimeField('Date updated', default=timezone.now)
    # TODO: remove update_week, calculate it from update date
    update_week = models.IntegerField('Week in year', default=timezone.now().isocalendar()[1])

    def __str__(self):
        return str(self.count)
