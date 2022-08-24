from django.db import models

# Create your models here.
class MBPost(models.Model):
    text = models.TextField()
    title = models.TextField()
    time = models.DateTimeField(primary_key=True)

class cragDestination(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    summary = models.TextField
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    history = models.TextField()