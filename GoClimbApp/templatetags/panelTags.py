
from django import template

register = template.Library()

from django.contrib.auth.models import User
from ..models import MBPost, MBPostLikeStatus, userProfile


@register.simple_tag
def getLevel(user : User) -> str:
    level = "Level "+str(userProfile.objects.get(userID=user).level)
    return level

@register.simple_tag
def getLiked(user: User, post:MBPost) ->bool:
    try:
       return MBPostLikeStatus.objects.get(
            FKUserProfile = userProfile.objects.get(userID=user), 
            FKMBPost = post).isLiked
    except MBPostLikeStatus.DoesNotExist:
        return False