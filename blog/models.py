from django.db import models
from django.utils.html import mark_safe

from account.models import User

class FileModel(models.Model):
    file = models.FileField(upload_to="file",verbose_name="فایل")
    def __str__(self):
        return f"{self.pk}"
    class Meta:
        ordering = ['-pk']
        verbose_name = "فایل"
        verbose_name_plural = "فایل ها"

# Create your models here.

class Category(models.Model):
    position = models.IntegerField(default=0 , verbose_name='پوزیشن')
    title = models.TextField(verbose_name="متن")

    def __str__(self):
        return f"{self.pk}--{self.title}"

    class Meta:
        verbose_name = "دسته بندی اصلی"
        verbose_name_plural = "دسته بندی های اصلی"

    def __str__(self):
        return f"{self.pk}--{self.title}"

class ImageHeader(models.Model):
    title_for_photo=models.TextField(blank=True,verbose_name="متن برای عکس")
    photo = models.ImageField(verbose_name="عکس")
    def image_tag(self):
            return mark_safe('<img src="%s"  height="100" />' % (self.photo.url))
    image_tag.short_description = 'Image'
    class Meta:
        ordering = ['-pk']
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"

    def __str__(self):
        return f"{self.pk}--{self.photo}"

class Blog(models.Model):
    imageBlog=models.ForeignKey(ImageHeader,verbose_name="عکس",blank=True,null=True,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category,blank=True,verbose_name="دسته بندی")
    like=models.ManyToManyField(User,blank=True,verbose_name="دسته بندی",related_name='like+Blog+')
    title=models.TextField(verbose_name="متن")
    body=models.TextField(verbose_name="متن بدنه")
    file = models.ManyToManyField(FileModel,blank=True,verbose_name="فایل")
    author = models.ForeignKey(User,verbose_name='نویسنده',blank=True,null=True,on_delete=models.CASCADE)


    
    def __str__(self):
        return f"{self.pk}--{self.title}"
    class Meta:
        ordering = ['-pk']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
    
    

