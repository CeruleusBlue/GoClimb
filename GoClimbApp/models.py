from django.db import models
from django.contrib.auth.models import User
from traitlets import default

# Create your models here.    
class cragDestination(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    summary = models.TextField()
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    history = models.TextField()

class cragFace(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    locationX = models.FloatField()
    locationY = models.FloatField()
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    FKCragDestination = models.ForeignKey(cragDestination, default=None, on_delete=models.CASCADE)

class cragRoute(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    grade = models.IntegerField()
    image = models.TextField(default="None")
    description = models.TextField()
    bolts = models.IntegerField()
    rating = models.IntegerField()
    length = models.IntegerField()
    ascents = models.IntegerField()
    firstAscent = models.TextField()
    FKCragFace = models.ForeignKey(cragFace, default=None, on_delete=models.CASCADE)

class cragRouteReview(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    FKCragRoute = models.ForeignKey(cragRoute, default=None, on_delete=models.CASCADE)
class userProfile(models.Model):
    userID = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)

class climbHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    FkUserProfile = models.ForeignKey(userProfile, default=None, on_delete=models.CASCADE)

class MBPost(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    title = models.TextField()
    time = models.DateTimeField()
    FKUserProfile = models.ForeignKey(userProfile, default=None, on_delete=models.CASCADE)

class MBPostLikeStatus(models.Model):
    FKUserProfile = models.ForeignKey(userProfile, default=None, on_delete=models.CASCADE)
    FKMBPost = models.ForeignKey(MBPost, default=None, on_delete=models.CASCADE)
    isLiked = models.BooleanField(default=False)
