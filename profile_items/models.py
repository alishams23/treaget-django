from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from extensions.utils import jalali_converter

# Create your models here.


class Skills(models.Model):
    title = models.TextField(blank=True,null=True)
    is_validate = models.BooleanField(default=True,blank=True,null=True)
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True,
                               related_name="Skills_author+")
    class Meta:
        verbose_name = "توانایی"
        verbose_name_plural = " توانایی ها"
       

    def __str__(self):
        return self.title


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


class Timeline(models.Model):
    title = models.CharField(max_length=400, blank=True,
                             null=True, verbose_name="تیتر")
    body = models.TextField(verbose_name="متن", blank=True, null=True)
    person = models.ForeignKey(
        User, verbose_name="طراح", on_delete=models.SET_NULL, null=True)
    createdAdd = models.DateField(auto_now_add=True)
    start = models.DateTimeField(blank=True, null=True, verbose_name="شروع")
    end = models.DateTimeField(blank=True, null=True, verbose_name="پایان")

    class Meta:
        verbose_name = " تایم لاین"
        verbose_name_plural = "تایم لاین ها"
        ordering = ["-createdAdd"]

    def __str__(self):
        return self.body

    def JSpublish(self):
        return jalali_converter(self.start)

    def JEpublish(self):
        return jalali_converter(self.end)

