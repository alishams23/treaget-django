from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Skills(models.Model):
    title = models.TextField(blank=True,null=True)



class ServiceSubset(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceSubsetAuthor")
    title = models.TextField(verbose_name="متن")
    price = models.BigIntegerField(default=0, verbose_name="قیمت")



class ServiceOptionMain (models.Model):
    title = models.TextField(verbose_name="متن")
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="خدمات دهنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceOptionMainAuthor")
    price = models.BigIntegerField(blank=True, null=True, verbose_name="قیمت")

    class Meta:
        verbose_name = "خدمات خدمات دهنده امکانات"
        verbose_name_plural = "امکانات خدمات خدمات دهندگان"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title



class Services(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="خدمات دهنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceAuthor")
    specialName = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="نام اختصاصی خدمات")
    hour = models.IntegerField(validators=[MinValueValidator(
        0)], blank=True, null=True, default="1", verbose_name="ساعت")
    minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(
        60)], blank=True, default="1", null=True, verbose_name="ساعت")
    price = models.BigIntegerField(blank=True, null=True, verbose_name="قیمت")
    priceEnd = models.BigIntegerField(
        blank=True, null=True, verbose_name="قیمت")
    subsetService = models.ManyToManyField(
        ServiceSubset, related_name="subsetServiceRelated", blank=True)
    serviceOption = models.ManyToManyField(
        ServiceOptionMain, related_name="ServiceOptionlastRelated", blank=True)

    class Meta:
        verbose_name = "خدمات خدمات دهنده"
        verbose_name_plural = "خدمات خدمات دهندگان"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.author.username

