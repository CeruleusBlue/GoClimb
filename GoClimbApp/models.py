from django.db import models

# Create your models here.
class MBPost(models.Model):
    text = models.TextField()