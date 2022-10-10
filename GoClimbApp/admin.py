from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(MBPost)
admin.site.register(MBPostLikeStatus)
admin.site.register(cragDestination)
admin.site.register(cragRoute)
admin.site.register(cragRouteReview)
admin.site.register(cragFace)
admin.site.register(userProfile)
admin.site.register(climbHistory)