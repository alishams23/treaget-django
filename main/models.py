from django.db import models
from django.utils.html import format_html
from account.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from extensions.utils import jalali_converter
from PIL import Image


# Create your models here.


class Category(models.Model):
    title = models.TextField(blank=True, null=True, verbose_name="ویژگی")
    position = models.IntegerField(
        verbose_name="پوزیشن", blank=True, null=True)
    createdadd = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title


class IPAddress(models.Model):
    # title = models.TextField(verbose_name="تیتر")
    ip_address = models.TextField(verbose_name="آدرس آی پی")


class Attributes(models.Model):
    Property = models.TextField(blank=True, null=True, verbose_name="ویژگی")
    position = models.IntegerField(
        verbose_name="پوزیشن", blank=True, null=True)

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی های محصول"
        ordering = ["position"]

    def __str__(self):
        return self.Property


class Price(models.Model):
    PRICETYPE_CHOICE = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"))
    title = models.TextField(verbose_name="تیتر")
    titleEN = models.SlugField(max_length=50, verbose_name="url تیتر")
    price = models.TextField(blank=True, null=True, verbose_name="قیمت")
    position = models.IntegerField(verbose_name="پوزیشن")
    category = models.ManyToManyField(
        Attributes, verbose_name="امکاناتی که دارد", related_name="T")
    category2 = models.ManyToManyField(
        Attributes, verbose_name="امکاناتی که ندارد", related_name="F")
    PriceType = models.CharField(max_length=1, choices=PRICETYPE_CHOICE, blank=True, null=True,
                                 verbose_name="عضو کدام محصول است؟")

    class Meta:
        verbose_name = "قیمت"
        verbose_name_plural = "قیمت ها"
        ordering = ["position"]

    def __str__(self):
        return self.title


class Products(models.Model):
    STATUS_CHOICES = (("p", "منتششر شده"), ("d", "پیشنویس شده"))
    TYPE_CHOICES = (("g", "گرافیک طراحی"), ("f", "فیلم و تیزر تبلیغاتی"), ("p", "عکاسی صنعتی"), ("o", "طراحی آفیس"),
                    ("w", "طراحی سایت"), ("s", "نرم افزار"), ("b", "ربات"), ("n", "شبکه و امنیت"))
    title = models.CharField(max_length=50, verbose_name="تیتر")
    question = models.TextField(verbose_name="سوال", blank=True, null=True)
    body = models.TextField(verbose_name="پاسخ", blank=True, null=True)
    position = models.IntegerField(verbose_name="پوزیشن")
    slug = models.SlugField(max_length=50, verbose_name="url مطلب")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="P", verbose_name="وضعیت محصول")
    category = models.ManyToManyField(Price, verbose_name="قیمت", blank=True)
    TypeProduct = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=True, null=True,
                                   verbose_name="وضعیت محصول")

    symbol = models.TextField(verbose_name="نماد", blank=True, null=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["position"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/studiosaran/{self.slug}/'


class Picture(models.Model):
    STATUS_CHOICES = (("p", "منتششر شده"), ("d", "پیشنویس شده"))
    category = models.ManyToManyField(
        Products, verbose_name="دسته بندی محصول", blank=True)
    like = models.ManyToManyField(
        User, verbose_name="تعداد لایک ها", blank=True, related_name="like_Picture")
    Visitor = models.ManyToManyField(
        User, verbose_name="بازدیده کننده", blank=True, related_name="Visitor_Picture")
    alt = models.CharField(blank=True, null=True,
                           max_length=200, verbose_name="تیتر")
    createdAdd = models.DateField(auto_now_add=True)
    position = models.IntegerField(
        default=1, blank=True, null=True, verbose_name="پوزیشن")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="p", verbose_name="وضعیت محصول")
    image = models.ImageField(upload_to="images", verbose_name="عکس محصول")
    author = models.ForeignKey(User, verbose_name="طراح", on_delete=models.SET_NULL, null=True,
                               related_name="author_Picture")

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"
        ordering = ("-position", "-createdAdd")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 800:
            img.thumbnail((800, 800))
            img.save(self.image.path)

    def picture_show(self):
        return format_html("<img src='{}' width=100 style='border-radius : 10px;' >".format(self.image.url))

    def Jpublish(self):
        return jalali_converter(self.createdAdd)


class OrderUser(models.Model):
    author = models.ForeignKey(User, verbose_name="نویسنده",
                               on_delete=models.SET_NULL, related_name="authorOrderUser", null=True)
    title = models.CharField(
        max_length=300, verbose_name="محصول درخواستی", blank=True, null=True)
    body = models.TextField(
        verbose_name="توضیحات محصول", blank=True, null=True)
    createdAdd = models.DateField(auto_now_add=True)
    service = models.ForeignKey("main.Service", verbose_name="نوع خدمات",
                                on_delete=models.SET_NULL, related_name="serviceOrderUser", null=True)
    designer = models.ForeignKey(User, verbose_name="طراح", on_delete=models.SET_NULL, null=True,
                                 related_name="designerOrderUser")
    price = models.BigIntegerField(verbose_name="قیمت")
    accept = models.BooleanField(verbose_name="تایید", blank=True, null=True)
    safePayment = models.ForeignKey("main.SafePayment", verbose_name="نوع خدمات", on_delete=models.SET_NULL,
                                    related_name="serviceOrderUser", null=True, blank=True)

    class Meta:
        verbose_name = "پیام سفارش از طراح"
        verbose_name_plural = "پیام های سفارش از طراح"
        ordering = ["-createdAdd"]


class contact(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام ونام خانوادگی")
    email = models.CharField(max_length=200, verbose_name="ایمیل")
    body = models.TextField(verbose_name="متن")
    createdadd = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "پیام ارتباط با ما"
        verbose_name_plural = "پیام های ارتباط با ما"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title


class BuyStudio(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    number = models.CharField(max_length=200, verbose_name="شماره ی تماس شما")
    image = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name="نمونه کار های مد نظر شما", blank=True,
                             null=True)
    imageNeed = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True,
                                 verbose_name="فایل های مورد نیاز")
    body = models.TextField(
        verbose_name="توضیحات محصول", blank=True, null=True)
    createdadd = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "فرم خرید"
        verbose_name_plural = "فرم های خرید"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.name


class FAQ(models.Model):
    TYPE_CHOICES = (("s", "استودیو "), ("p", "برنامه نویسی"),
                    ("m", "صفحه ی اصلی"), ("a", "اکانت"))
    TypeFAQ = models.CharField(
        max_length=1, choices=TYPE_CHOICES, blank=True, null=True, verbose_name="محل FAQ")
    title = models.CharField(max_length=300, verbose_name="تیتر FAQ")
    body = models.TextField(verbose_name="بدنه ی FAQ")
    createdadd = models.DateField(auto_now_add=True)
    position = models.IntegerField(
        blank=True, null=True, verbose_name="پوزیشن")

    class Meta:
        verbose_name = "فرم FAQ"
        verbose_name_plural = "فرم های FAQ"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title


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


class ServiceFacilities (models.Model):
    title = models.TextField(verbose_name="متن")
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="خدمات دهنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceFacilitiesAuthor")
    price = models.BigIntegerField(blank=True, null=True, verbose_name="قیمت")

    class Meta:
        verbose_name = "خدمات خدمات دهنده امکانات"
        verbose_name_plural = "امکانات خدمات خدمات دهندگان"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title


class Service(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="خدمات دهنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceAuthor")
    nameProduct = models.ForeignKey(Products, verbose_name="نوع خدمات", on_delete=models.SET_NULL, blank=True,
                                    null=True, related_name="NameProduct")
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
        "main.ServiceSubset", related_name="subsetServiceRelated", blank=True)
    serviceFacilities = models.ManyToManyField(
        ServiceFacilities, related_name="ServiceFacilitiesRelated", blank=True)

    class Meta:
        verbose_name = "خدمات خدمات دهنده"
        verbose_name_plural = "خدمات خدمات دهندگان"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.author.username


class ServiceSubset(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True,
                               related_name="ServiceSubsetAuthor")
    title = models.TextField(verbose_name="متن")
    price = models.BigIntegerField(default=0, verbose_name="قیمت")


class Blog(models.Model):
    createdadd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True,
                               related_name="BlogAuthor")
    title = models.CharField(max_length=200, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن")
    image = models.ImageField(upload_to="images/Blog",
                              verbose_name="عکس ", blank=True, null=True)
    position = models.IntegerField(
        blank=True, null=True, verbose_name="پوزیشن")

    class Meta:
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ ها"
        ordering = ["-createdadd"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 600:
                img.thumbnail((600, 600))
                img.save(self.image.path)
        except:
            pass


class Rules(models.Model):
    createdAdd = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن")

    class Meta:
        verbose_name = "قانون"
        verbose_name_plural = "قوانین"
        ordering = ["-createdAdd"]

    def __str__(self):
        return self.title


class Accept(models.Model):
    time = models.TextField(verbose_name="زمان انجام ")
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True)
    createdAdd = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "قبولی درخواست"
        verbose_name_plural = "قبولی های درخواست"
        ordering = ["-createdAdd"]


class Request(models.Model):
    title = models.TextField(verbose_name="عنوان")
    body = models.TextField(verbose_name="عنوان")
    createdAdd = models.DateField(auto_now_add=True)
    price = models.BigIntegerField(verbose_name="قیمت")
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True)
    subcategories = models.ManyToManyField(
        Accept, related_name="subcategoriesRelated", blank=True)

    class Meta:
        verbose_name = "درخواست پروژه"
        verbose_name_plural = "درخواست های پروژه"
        ordering = ["-createdAdd"]


class SubsetTrello(models.Model):
    title = models.TextField(verbose_name="عنوان")
    createdAdd = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "زیرمجموعه ترلو"
        verbose_name_plural = "زیرمجموعه ترلو ها"
        ordering = ["-createdAdd"]


class Trello(models.Model):
    title = models.TextField(verbose_name="عنوان")
    createdAdd = models.DateField(auto_now_add=True)
    forSafePayment = models.ForeignKey("main.SafePayment", verbose_name="برای خرید", on_delete=models.SET_NULL,
                                       null=True, related_name="forSafePayment")
    subsetTrello = models.ManyToManyField(
        SubsetTrello, verbose_name="زیر مجموعه", blank=True)

    class Meta:
        verbose_name = "ترلو"
        verbose_name_plural = "ترلو ها"
        ordering = ["-createdAdd"]


class SafePayment(models.Model):
    description = models.TextField(
        verbose_name="توضیحات", blank=True, null=True)
    price = models.BigIntegerField(verbose_name="قیمت")
    createdAdd = models.DateField(auto_now_add=True)
    receiver = models.ForeignKey(User, verbose_name="دریافت کننده", on_delete=models.SET_NULL, null=True,
                                 related_name="receiver")
    sender = models.ForeignKey(User, verbose_name="ارسال کننده", on_delete=models.SET_NULL, null=True,
                               related_name="Sender")
    paymentBoolean = models.BooleanField(
        default=False, verbose_name="بولین گیرنده", blank=True, null=True)
    senderBoolean = models.BooleanField(
        default=False, verbose_name="بولین فرستنده", blank=True, null=True)

    class Meta:
        verbose_name = "پرداخت امن"
        verbose_name_plural = "پرداخت های امن"
        ordering = ["-createdAdd"]


class Dispute(models.Model):
    description = models.TextField(
        verbose_name="توضیحات", blank=True, null=True)
    Result = models.TextField(verbose_name="نتیجه", blank=True, null=True)
    createdAdd = models.DateField(auto_now_add=True)
    safePayment = models.ForeignKey(SafePayment, verbose_name="دریافت کننده", on_delete=models.SET_NULL, null=True,
                                    related_name="safePayment")
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True,
                               related_name="author")

    class Meta:
        verbose_name = "اختلاف"
        verbose_name_plural = "اختلافات"
        ordering = ["-createdAdd"]
