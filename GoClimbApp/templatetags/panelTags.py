
from django import template
from django.templatetags.static import static

register = template.Library()

from django.contrib.auth.models import User
from ..models import MBPost, MBPostLikeStatus, userProfile


@register.simple_tag
def getLevel(user : User):
    """Returns the Level of the User"""
    return userProfile.objects.get(userID=user).level

@register.simple_tag
def getUserName(user: User):
    """Returns the User Name of the User"""
    return user.username.capitalize()

@register.simple_tag
def getLiked(user, post):
    """Returns the like icon to diplay based on whether a user likes a post or not"""
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