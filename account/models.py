from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from django.utils.html import format_html



# Create your models here.


class User(AbstractUser):
    is_author = models.BooleanField(verbose_name="وضعیت :نویسندگی", default=False)
    is_designer = models.BooleanField(verbose_name="وضعیت :طراح", default=False)
    is_programer = models.BooleanField(verbose_name="وضعیت :برنامه نویس", default=False)
    is_Colleague = models.BooleanField(verbose_name="وضعیت :همکار", default=False)
    isVerified = models.BooleanField(verbose_name="وضعیت :تایید شده", default=False,blank=True,null=True)
    ServiceProvider = models.BooleanField(verbose_name="وضعیت :خدمات دهنده", default=True, blank=True, null=True)
    special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه")
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', verbose_name="عکس پروفایل", blank=True, null=True)
    bio = models.TextField(verbose_name="بیو کاربر", blank=True, null=True)
    category = models.ManyToManyField("main.Category", verbose_name="عضو کدام دسته بندیست", blank=True,
                                      related_name="CategoryMainRelated")
    numberVisitors = models.ManyToManyField("main.IPAddress", verbose_name="بازدید ها", blank=True, related_name="hits")
    ability = models.ManyToManyField("main.Products", verbose_name="توانایی ها", blank=True, related_name="abl")
    like = models.ManyToManyField("main.Picture", verbose_name="لایک ها", blank=True, related_name="likeRelated")
    followers = models.ManyToManyField('User', blank=True, related_name='followers_user', verbose_name="followers")
    following = models.ManyToManyField('User', blank=True, related_name='following_user', verbose_name="following")
    cash = models.BigIntegerField(verbose_name="پول", default=0, blank=True, null=True)
    verify_phone = models.BooleanField(verbose_name="تایید شماره تلفن", blank=True, null=True)
    verify_phone_code = models.BigIntegerField(verbose_name="کد تایید", blank=True, null=True)
    phone_number = models.BigIntegerField(verbose_name="شماره تلفن", blank=True, null=True)
    count_sms=models.IntegerField(verbose_name="تعداد پیامک",default=0)

        
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True
    is_special_user.short_description = 'کاربر ویژه'

    def get_absolute_url(self):
        return f'/p/{self.username}/'

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            # width, height = img.size
            # if height > width:
            #     h2 = height / 2
            #     h4 = h2 / 2
            #     border = (0, h4, width, h4 * 3)
            #     img.crop(border)
            if img.height > 500:
                img.thumbnail((500, 500))
                img.save(self.image.path)
        except:
            pass
    def picture_show(self):
        try:
            data = format_html("<img src='{}' width=100 style='border-radius : 10px;' >".format(self.image.url))
        except:
            data="null"
        return data



class Message(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="فرستنده", on_delete=models.SET_NULL, null=True,
                               related_name="messageAuth")
    receiver = models.ForeignKey(User, verbose_name="گیرنده", on_delete=models.SET_NULL, null=True,
                                 related_name="receiveAuth")
    text = models.TextField(verbose_name="متن", blank=True, null=True)
    read = models.BooleanField(verbose_name="تایید",default=False)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام"
        ordering = ["-createdadd"]

        def __str__(self):
            return self.text


class Notification(models.Model):
    createdAdd = models.DateField(auto_now_add=True)
    receiver = models.ForeignKey(User, verbose_name="گیرنده", on_delete=models.SET_NULL, null=True,
                               related_name="authorNotification")
    title = models.TextField(verbose_name="تیتر", blank=True, null=True)
    body = models.TextField(verbose_name="متن", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="یوزر", on_delete=models.SET_NULL, null=True,
                             related_name="userNotification")
    readingStatus = models.BooleanField(default=False, verbose_name="وضعیت خواندن")
    url = models.TextField(verbose_name="آدرس", blank=True, null=True)

    class Meta:
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشن ها"
        ordering = ["-createdAdd"]

        def __str__(self):
            return self.title
