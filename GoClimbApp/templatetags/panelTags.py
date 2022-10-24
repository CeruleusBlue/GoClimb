
from django import template
from django.templatetags.static import static

register = template.Library()

from django.contrib.auth.models import User
from ..models import MBPost, MBPostLikeStatus, userProfile


@register.simple_tag
def getLevel(user : User):
    return str(userProfile.objects.get(userID=user).level)

@register.simple_tag
def getUserName(user: User):
    return user.username.capitalize()

@register.simple_tag
def getLiked(user, post):
    isLiked = None
    try:
        isLiked = MBPostLikeStatus.objects.get(
            FKUserProfile = userProfile.objects.get(userID=user), 
            FKMBPost = post).isLiked
    except MBPostLikeStatus.DoesNotExist:
        pass
    finally:
        if(isLiked):
          return static('images/heart.png')
        else:
          return static('images/heart-empty.png')