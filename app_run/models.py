from django.contrib.auth.models import User
from django.db import models

class Run(models.Model):
    class StatusChoices(models.TextChoices):
        INIT = 'init', 'init'
        IN_PROGRESS = 'in_progress', 'in_progress'
        FINISHED = 'finished', 'finished'

    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    comment = models.TextField()
    status = models.CharField(max_length=11, choices=StatusChoices, default=StatusChoices.INIT)
    created_at = models.DateTimeField(auto_now_add=True)


class AthleteInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.TextField(null=True)
    weight = models.IntegerField(null=True)


class Challenge(models.Model):
    full_name = models.CharField(max_length=255)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)