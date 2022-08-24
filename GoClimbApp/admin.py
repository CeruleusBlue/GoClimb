from django.contrib import admin

from .models import MBPost, cragDestination, cragFace, cragRoute, cragRouteReview, cragFace
# Register your models here.
admin.site.register(MBPost)
admin.site.register(cragDestination)
admin.site.register(cragRoute)
admin.site.register(cragRouteReview)
admin.site.register(cragFace)