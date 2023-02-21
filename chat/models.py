from django.db import models
from account.models import User
# Create your models here.





class Chat (models.Model):
    room_name = models.CharField(blank=True, max_length=50)
    members = models.ManyToManyField(User,  blank=True)
    
    
    def __str__(self):
        return self.room_name
    



class Message(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def last_message(self, room_name):
        return Message.objects.filter(related_chat__room_name=room_name)

    def __str__(self):
        return self.author.username


    