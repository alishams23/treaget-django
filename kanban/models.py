from django.db import models
from account.models import User
# Create your models here.



class KanbanListItem(models.Model):
    title = models.TextField(verbose_name="عنوان")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "زیرمجموعه ترلو"
        verbose_name_plural = "زیرمجموعه ترلو ها"
        ordering = ["-pk"]


class KanbanList(models.Model):
    title = models.TextField(verbose_name="عنوان")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(KanbanListItem,blank=True)


class Kanban(models.Model):
    title = models.TextField(verbose_name="عنوان",default="کانبان")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User,related_name="members_kanban+")
    observer = models.ManyToManyField(User,blank=True,related_name="observe_kanban+")
    lists = models.ManyToManyField(
        KanbanList, verbose_name="زیر مجموعه", blank=True)

    class Meta:
        verbose_name = "ترلو"
        verbose_name_plural = "ترلو ها"
        ordering = ["-pk"]
