from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(User)
admin.site.register(Pbi)
admin.site.register(DevTeamMember)
admin.site.register(ProductOwner)
