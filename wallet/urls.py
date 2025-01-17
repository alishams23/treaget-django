from django.urls import path, include
from . import views
app_name="wallet"
urlpatterns = [
    path('', views.wallet, name="wallet"),
    path('IncreaseMoney/', views.increaseMoney, name="increaseMoney"),
    path('IncreaseMoney/<int:amount>/', views.increaseMoney, name="increaseMoneyAmount"),
    path('WithdrawMoney/', views.withdrawMoney, name="WithdrawMoney"),
    path('verify/<int:amount>/', views.verify, name="verify"),
    path('enamad/', views.enamad, name="verify"),
    path('wWithdrawMoneyApi/', views.wWithdrawMoneyApi.as_view(), name="wWithdrawMoneyApi"),
    path('listTransaction/', views.listTransaction.as_view(), name="listTransaction"),
    
]
