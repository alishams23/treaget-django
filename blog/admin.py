from django.contrib import admin
from django.db.models import fields
from .models import *
# Register your models here.

class FileAdmin(admin.ModelAdmin):
    list_display=("file",)
    

admin.site.register(FileModel,admin_class=FileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=("title","id")
    

admin.site.register(Category,admin_class=CategoryAdmin)

class PictureBlogAdmin(admin.ModelAdmin):
    list_display=("id","photo")
    

admin.site.register(ImageHeader,admin_class=PictureBlogAdmin)

class BlogAdmin(admin.ModelAdmin):
    filter_horizontal=('category',"file")
    list_display=("title","body")
    search_fields =("title",)

admin.site.register(Blog,admin_class=BlogAdmin)

