from django.db import models
from django.utils import timezone
from account.models import User



# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(verbose_name='نام', max_length=30)
    last_name = models.CharField(verbose_name='نام خانواگی', max_length=30)
    email = models.EmailField(verbose_name='ایمیل', blank=True)
    mobile_number = models.CharField(verbose_name='تلفن همراه', max_length=11, help_text="0912 345 6789")
    phone_number = models.CharField(verbose_name='تلفن ثابت', max_length=11, blank=True, null=True)
    birth_day = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    adress = models.TextField(verbose_name="آدرس", null=True, blank=True)
    card_number = models.CharField(verbose_name="شماره کارت", max_length=16,default='', blank=True, null=True)
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True, related_name="ContactAuthor")  

    def __str__(self):
        return self.first_name
    

class Sell(models.Model):
    SELL_CHOISES = (
        ('Nqdi', 'پرداخت نقدی'),
        ('Card', 'پرداخت آنلاین'),
        ('Chek', 'پرداخت چکی'),
    )

    product = models.CharField(verbose_name='محصول', max_length=200)
    price = models.IntegerField(verbose_name='قیمت', )
    costumer = models.ManyToManyField(Contact,verbose_name='نام خریدار', related_name="Contact")
    sell_info = models.TextField(verbose_name='شرح فروش', null=True, blank=True)
    sell_metode = models.CharField(verbose_name='روش پرداخت', max_length=4, choices=SELL_CHOISES)
    pay_key = models.CharField(verbose_name='شماره فروش', max_length=30, null=True, blank=True)
    date = models.DateField(verbose_name='تاریخ', default=timezone.now, null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="نویسنده",default='', on_delete=models.SET_NULL, null=True, related_name="SellAuthor")

    # remember_time = models.TimeField(verbose_name='ساعت', default=timezone.now)


class Chek(models.Model):
    receiver = models.CharField(verbose_name="دروجه", max_length=200)
    sender = models.CharField(verbose_name="دهنده چک", max_length=200)
    price = models.IntegerField(verbose_name="مبلغ(ریال)")
    date = models.DateField(verbose_name="تاریخ چک", null=True, blank=True)
    date_now = models.DateField(verbose_name="تاریخ صدور چک", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="نویسنده",default='', on_delete=models.SET_NULL, null=True, related_name="ChekAuthor")



class Todo(models.Model):
    title = models.CharField(verbose_name='موضوع', max_length=200)
    body = models.TextField(verbose_name='شرح', blank=True, null=True)
    remember_date = models.DateField(verbose_name='تاریخ', default=timezone.now)
    remember_time = models.TimeField(verbose_name='ساعت', default=timezone.now)






class Company(models.Model):
    author = models.ForeignKey(User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True, related_name="CompanyAuthor")
    name = models.CharField(verbose_name="نام شرکت", max_length=100)
    manager = models.ManyToManyField(Contact, verbose_name="مدیرعامل", related_name="manager")
    assistant = models.ManyToManyField(Contact, verbose_name="معاون", related_name="assistant") 
    accountant = models.ManyToManyField(Contact, verbose_name="حسابدار", related_name="AccountantRelated")
    clerk = models.ManyToManyField(Contact, verbose_name="منشی", related_name="clerk")
    supplier = models.ManyToManyField(Contact, verbose_name="کارپرداز", related_name="Supplier")
    marketer =  models.ManyToManyField(Contact, verbose_name="بازاریاب", related_name="Marketer")
    guard = models.ManyToManyField(Contact, verbose_name="حراست", related_name="Guard")
    services = models.ManyToManyField(Contact, verbose_name="خدمات", related_name="Services")
    storekeeper = models.ManyToManyField(Contact, verbose_name="انباردار", related_name="storekeeper")
    
    def __str__(self):
        return self.name

