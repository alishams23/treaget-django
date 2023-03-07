from django.db import models
from account.models import User
# Create your models here.





class Chat(models.Model):
    room_name = models.CharField(blank=True, max_length=50)
    members = models.ManyToManyField(User,  blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.room_name
    



class Message(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE , verbose_name="نویسنده")
    content = models.TextField(verbose_name="متن")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True,verbose_name="اطلاعات گفتگو")
    read = models.BooleanField(verbose_name="تایید",default=False)
    def last_message(self, room_name):
        return Message.objects.filter(related_chat__room_name=room_name).order_by("pk")

    def __str__(self):
        return self.author.username


    