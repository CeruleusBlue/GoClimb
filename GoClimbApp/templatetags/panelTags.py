
from django import template

register = template.Library()

from django.contrib.auth.models import User
from ..models import userProfile


@register.simple_tag
def getLevel(user : User) -> str:
    level = "Level "+str(userProfile.objects.get(userID=user).level)
    return level