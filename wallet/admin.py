from django.contrib import admin
from .models import *
# Register your models here.

class listTransactionAdmin(admin.ModelAdmin):
    list_display = ("user",)



admin.site.register(PaymentWalletB, listTransactionAdmin)

