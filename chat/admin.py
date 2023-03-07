from django.contrib import admin
from .models import *
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)


class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ("members",)


admin.site.register(Chat, ChatAdmin)
