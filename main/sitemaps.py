from django.contrib.sitemaps import Sitemap

from django.shortcuts import reverse
from .models import Products
from account.models import User

class staticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority: 1.0
    def items(self):
        return ['main:main', 'main:contact', 'account:login', 'account:register']

    def location(self,item):
        return reverse(item)

class SnippetSitemap(Sitemap):
    changefreq = "weekly"
    def items(self):
        return Products.objects.filter(status="p") 

class PrpfileSitemap(Sitemap):
    changefreq = "always"
    def items(self):
        return User.objects.all()