from django.contrib import admin
from .models import *
# Register your models here.




class ServiceAdmin(admin.ModelAdmin):
    list_display = ("author","pk")
    search_fields = ("-createdadd",)


admin.site.register(Services, ServiceAdmin)


class ServiceFacilitiesAdmin(admin.ModelAdmin):
    list_display = ("title","pk")


admin.site.register(ServiceOptionMain, ServiceFacilitiesAdmin)


class ServiceSubsetAdmin(admin.ModelAdmin):
    pass


admin.site.register(ServiceSubset, ServiceSubsetAdmin)




class TimelineAdmin(admin.ModelAdmin):
    list_display = ( "pk","body","title","person")


admin.site.register(Timeline, TimelineAdmin)

