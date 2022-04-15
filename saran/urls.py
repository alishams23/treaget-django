"""saran URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import staticViewSitemap , SnippetSitemap,PrpfileSitemap
# import adminlte3
from django.contrib.auth import views

sitemaps={
    'static':staticViewSitemap,
    # 'snippet':SnippetSitemap,
    # 'profile':PrpfileSitemap
}


urlpatterns = [
    path('adminsh/', admin.site.urls),
    # path('adminl/', adminlte3.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('api/wallet/', include('wallet.urls'), name="wallet"),
    
    path('', include('main.urls')),
    path('account/', include('account.urls'), name="account"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # path('accounting/', include('accounting.urls'), name="accounting"),

    path('api/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]



