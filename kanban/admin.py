from django.contrib import admin
from .models import *
# Register your models here.

class KanbanAdmin(admin.ModelAdmin):
    filter_horizontal=("members","observer","lists")
    


admin.site.register(Kanban, KanbanAdmin)


class KanbanListAdmin(admin.ModelAdmin):
    pass


admin.site.register(KanbanList, KanbanListAdmin)


class KanbanListItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(KanbanListItem, KanbanListItemAdmin)
