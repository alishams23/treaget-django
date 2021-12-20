from django.db import models
from django.utils import timezone
from account.models import User


# Create your models here.

# class PaymentWalletA(models.Model):
#     payStatus = models.BooleanField(verbose_name="وضعیت ", default=True)
#     typePayment = models.BooleanField(verbose_name="وضعیت ", default=True)
#     name = models.TextField(blank=True, null=True, verbose_name="نام")
#     cash = models.BigIntegerField(verbose_name="مقدار تراکنش")
#     cardNumber = models.BigIntegerField(verbose_name="شماره کارت")
#     timePayment = models.DateTimeField(default=timezone.now, verbose_name="زمان انجام تراکنش")
#     user = models.ForeignKey(User, related_name='UserPayment', verbose_name="شخص", null=True, on_delete=models.SET_NULL)
#     RefID = models.TextField(verbose_name="RefID", blank=True, null=True)

#     class Meta:
#         verbose_name = "تراکنش کیف پول"
#         verbose_name_plural = "تراکنش های کیف پول"
#         ordering = ["-timePayment"]


class PaymentWalletB(models.Model):
    payStatus = models.BooleanField(verbose_name="وضعیت ", default=True)
    typePayment = models.BooleanField(verbose_name="وضعیت ", default=True)
    name = models.TextField(blank=True, null=True, verbose_name="نام")
    cash = models.BigIntegerField(verbose_name="مقدار تراکنش")
    cardNumber = models.BigIntegerField(verbose_name="شماره کارت")
    timePayment = models.DateTimeField(default=timezone.now, verbose_name="زمان انجام تراکنش")
    user = models.ForeignKey(User, related_name='UserPaymentB', verbose_name="شخص", null=True, on_delete=models.SET_NULL)
    RefID = models.TextField(verbose_name="RefID", blank=True, null=True)

    class Meta:
        verbose_name = "تراکنش کیف پول"
        verbose_name_plural = "تراکنش های کیف پول"
        ordering = ["-timePayment"]
