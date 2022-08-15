from django.db import models

# Create your models here.
class MBPost(models.Model):
    text = models.TextField()
    title = models.TextField()
    time = models.DateTimeField(primary_key=True)