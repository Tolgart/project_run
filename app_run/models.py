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