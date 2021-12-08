from django.contrib import admin
from .models import *
# from accounting.models import Sell, Contact, Chek
from django.utils.translation import ngettext
from django.contrib import messages

# change template tag panel admin
admin.site.site_header = "پنل مدیریت"


# Register your models here.
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d محصول منتشر شد',
        '%d محصول منتشر شد',
        updated,
    ) % updated, messages.SUCCESS)


make_published.short_description = "منتشر کردن محصول شما"


def make_define(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d محصول پیشنویس شد',
        '%d محصول پیشنویس شد',
        updated,
    ) % updated, messages.SUCCESS)


make_define.short_description = "پیشنویس کردن محصول شما"


class ProductsAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status")
    list_filter = ("status",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_define]


admin.site.register(Products, ProductsAdmin)


class PictureAdmin(admin.ModelAdmin):
    list_display = ("alt", "position", "picture_show", "author", "createdAdd")
    search_fields = ("alt",)


admin.site.register(Picture, PictureAdmin)


class AttributesAdmin(admin.ModelAdmin):
    list_display = ("position",)


admin.site.register(Attributes, AttributesAdmin)


class PriceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "PriceType", "titleEN")
    search_fields = ("title",)
    prepopulated_fields = {"titleEN": ("title",)}


admin.site.register(Price, PriceAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ( "name", "email", "body")


admin.site.register(contact, ContactAdmin)


class BuyStudioAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "body")
    search_fields = ("title",)


admin.site.register(BuyStudio, BuyStudioAdmin)


class RulesAdmin(admin.ModelAdmin):
    list_display = ("title", "body")
    search_fields = ("title",)


admin.site.register(Rules, RulesAdmin)


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("ip_address","id")
    search_fields = ("ip_address",)


admin.site.register(IPAddress, IPAddressAdmin)


class OrderUserAdmin(admin.ModelAdmin):
    list_display = ("designer","pk")
    search_fields = ("-createdAdd",)


admin.site.register(OrderUser, OrderUserAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display = ("TypeFAQ", "title", "position")
    search_fields = ("-createdadd",)


admin.site.register(FAQ, FAQAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("author", "nameProduct","pk")
    search_fields = ("-createdadd",)


admin.site.register(Service, ServiceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("-createdadd",)


admin.site.register(Category, CategoryAdmin)


# class AccountingContactAdmin(admin.ModelAdmin):
#     list_display=("first_name", "last_name",)

# admin.site.register(Contact, AccountingContactAdmin)


# class AccountingSellAdmin(admin.ModelAdmin):
#     list_display=("product", "price")

# admin.site.register(Sell, AccountingSellAdmin)


# class AccountingChekAdmin(admin.ModelAdmin):
#     list_display=("receiver", "sender", "price",)

# admin.site.register(Chek, AccountingChekAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "body")


admin.site.register(Blog, BlogAdmin)


class TimelineAdmin(admin.ModelAdmin):
    list_display = ( "pk","body","title","person")


admin.site.register(Timeline, TimelineAdmin)


class RequestAdmin(admin.ModelAdmin):
    list_display = ("title", "body")


admin.site.register(Request, RequestAdmin)


class AcceptAdmin(admin.ModelAdmin):
    list_display = ("time",)


admin.site.register(Accept, AcceptAdmin)


class SafePaymentAdmin(admin.ModelAdmin):
    list_display = ("sender",)


admin.site.register(SafePayment, SafePaymentAdmin)


class TrelloAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Trello, TrelloAdmin)


class SubsetTrelloAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(SubsetTrello, SubsetTrelloAdmin)


class DisputeAdmin(admin.ModelAdmin):
    list_display = ("author",)


admin.site.register(Dispute, DisputeAdmin)


class ServiceFacilitiesAdmin(admin.ModelAdmin):
    list_display = ("title","pk")


admin.site.register(ServiceOptionMain, ServiceFacilitiesAdmin)


class SpamAdmin(admin.ModelAdmin):
    list_display = ("author",)


admin.site.register(Spam, SpamAdmin)