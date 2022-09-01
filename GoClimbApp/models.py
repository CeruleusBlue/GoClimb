from django.db import models
from django.contrib.auth.models import User

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

class cragRoute(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    grade = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to = "static/images/cragRoutes")
    description = models.TextField()
    bolts = models.IntegerField()
    rating = models.IntegerField()
    length = models.IntegerField()
    ascents = models.IntegerField()
    firstAscent = models.TextField()
    cragDestinationFK = models.ForeignKey(cragDestination, default=None, on_delete=models.CASCADE)

class cragRouteReview(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    cragRouteFK = models.ForeignKey(cragRoute, default=None, on_delete=models.CASCADE)

class cragFace(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    locationX = models.FloatField()
    locationY = models.FloatField()
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    ethics = models.TextField()
    cragRouteFK = models.ForeignKey(cragRoute, default=None, on_delete=models.CASCADE)

class userProfile(models.Model):
    userID = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)

class climbHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    userProfileFk = models.ForeignKey(userProfile, default=None, on_delete=models.CASCADE)