from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from account.views import User
from wallet.models import PaymentWalletA
from zeep import Client

# Create your views here.
MERCHANT = 'd16f23cc-5cde-4cfb-bd0d-f5121b0887c8'
email = ''  # Optional
mobile = ''  # Optional
CallbackURL = 'http://treaget.com/wallet/verify/'  # Important: need to edit for realy server.
description = "شارژ کیف پول تریگت"  # Required


@login_required
def wallet(request):
    context = {

    }
    return render(request, 'desk/wallet.html', context)


@login_required
def withdrawMoney(request):
    if request.method == "POST":
        amount = request.POST.get("number")
        cardNumber = request.POST.get("cardNumber")
        name = request.POST.get("name")
        if int(amount) > request.user.cash:
            context = {
                'error': "مبلغ انتخابی بیشتر از مبلغ موجود در کیف پول شماست"
            }
            return render(request, 'desk/wallet.html', context)
        elif int(amount) == 0:
            context = {
                'error': "مبلغ انتخابی نباید صفر باشد"
            }
            return render(request, 'desk/wallet.html', context)
        elif int(amount) <= request.user.cash:
            PaymentWallet = PaymentWalletA(user=request.user, cash=amount, typePayment=False, cardNumber=cardNumber,
                                              name=name)
            context = {
                'success': "عملیات موفقیت آمیز بود . پرداخت حداکثر ظرف 48 ساعت دیگر انجام می شود"
            }
            return render(request, 'desk/wallet.html', context)
    return redirect('/wallet')


@login_required
def increaseMoney(request, amount=None):
    client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

    if amount is None:
        amount = request.POST.get("number")
    result = client.service.PaymentRequest(MERCHANT, int(amount), description, email, mobile,
                                           CallbackURL + str(amount))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse(
            'خطایی در انجام تراکنش مشاهده شد لطفا مدتی دیگر مجدد امتحان کنید \n Error code: ' + str(result.Status))


def verify(request, amount):
    client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            UserPay = request.user
            UserPay.cash = UserPay.cash + int(amount)
            paymentResult = PaymentWalletA.objects.create(user=request.user, cash=amount, RefID=str(result.RefID))
            paymentResult.save()
            return redirect("/wallet/")
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
