from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message, Notification

UserAdmin.fieldsets += (
    ('فیلد های خاص من', {
        "fields": (
            'is_author',
            'special_user',
            'is_designer',
            'image',
            'ability',
            'numberVisitors',
            'is_programer',
            'is_Colleague',
            'bio',
            'category',
            'cash',
            'followers',
            'following',
            'ServiceProvider',
            'isVerified',
            'verify_phone',
            'verify_phone_code',
            'phone_number',
            'count_sms',

        ),
    }),
)

UserAdmin.list_display += ('is_author', 'is_special_user',"picture_show")
UserAdmin.list_filter += ('date_joined', )

admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "createdadd")
    search_fields = ("text",)


admin.site.register(Message, MessageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("receiver", "createdAdd")
    search_fields = ("title",)


admin.site.register(Notification, NotificationAdmin)
