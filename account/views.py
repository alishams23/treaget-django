from django.shortcuts import render, get_object_or_404
from extensions.utils import jalaliConvertToGregorian
from itertools import chain
from operator import attrgetter
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.models import Picture, FAQ, OrderUser, Timeline, Category, Request, SafePayment, Dispute, \
    Accept, Trello, SubsetTrello
from .forms import PictureForm, UserForm, UserAddForm, TimelineForm, SafePaymentForm, DisputeForm, \
    RequestForm, AcceptForm, TrelloForm, SubsetTrelloForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Message, Notification
from django.db.models import Q
from main.views import deleteDuplicate
from main.forms import OrderUserForm
import datetime
from django.core.mail import send_mail
from extensions.notification import notificationAdd
from django.db.models import Count



def safePaymentAddTrello(forSafePayment):
    TrelloInstance1 = Trello(title="در لیست انجام", forSafePayment=forSafePayment)
    TrelloInstance1.save()
    TrelloInstance2 = Trello(title="در حال انجام", forSafePayment=forSafePayment)
    TrelloInstance2.save()
    TrelloInstance3 = Trello(title="انجام شده", forSafePayment=forSafePayment)
    TrelloInstance3.save()


@login_required
def home(request):
    firstData = Picture.objects.filter(
        Q(author__id__in=request.user.following.all()) | Q(author=request.user))
    secondData = Request.objects.filter(Q(author__id__in=request.user.following.all()) | Q(author=request.user))
    result_list = sorted(
        chain(firstData, secondData),
        key=attrgetter('createdAdd'), reverse=True)[0:5]
    if len(result_list) == 0:
        result_list = Picture.objects.all()[0:5]
    context = {
        "page": "main",
        "posts": result_list,
        'FAQs': FAQ.objects.filter(TypeFAQ='a').order_by('position'),
        'UserRequirements': User.objects.filter(~Q(followers=request.user)).order_by("-pk")[0:5],
        'addPost': PictureForm(),
        # 'PictureRequments':Picture.objects.all().order_by("-pk")[0:4],
    }
    suggestion = User.objects.filter(~Q(followers=request.user) & ~Q(image="")).order_by("?")[0:8]
    context.update({'suggestion': suggestion})
    return render(request, "registration/main.html", context)


@login_required
def post(request, pk):
    if pk :
        result = Picture.objects.get(pk=pk)
        context = {
            "posts": [result],
        }
        return render(request, "registration/post.html", context)



@login_required
def desk(request):
    context = {}
    if request.user.ServiceProvider:
        context = {
            "pictureCheck": False,
            "timelineCheck": False,
            "serviceCheck": False,
            "numberSafePayment": SafePayment.objects.filter(receiver=request.user).count(),
            "numberOrders": OrderUser.objects.filter(designer=request.user).count(),
            "numberPicture": Picture.objects.filter(author=request.user).count(),
            "numberDoProject": SafePayment.objects.filter(receiver=request.user, senderBoolean=True
                                                          , paymentBoolean=True).count(),
            "numberDoingProject": SafePayment.objects.filter(receiver=request.user, paymentBoolean=False).count(),
            # "numberService": Services.objects.filter(author=request.user).count(),

        }
        print((len(Picture.objects.filter(author=request.user))))
        if len(Picture.objects.filter(author=request.user)) == 0:
            context.update({"pictureCheck": True})
        if len(Timeline.objects.filter(person=request.user)) == 0:
            context.update({"timelineCheck": True})
        # if len(Services.objects.filter(author=request.user)) == 0:
        #     context.update({"serviceCheck": True})
    else:
        context = {
            "pictureCheck": False,
            "timelineCheck": False,
            "serviceCheck": False,
            "numberSafePayment": SafePayment.objects.filter(sender=request.user).count(),
            "numberOrders": OrderUser.objects.filter(author=request.user).count(),
            "numberRequest": Request.objects.filter(author=request.user).count(),
            "numberDoProject": SafePayment.objects.filter(sender=request.user, senderBoolean=True
                                                          , paymentBoolean=True).count(),
            "numberDoingProject": SafePayment.objects.filter(sender=request.user, paymentBoolean=False).count(),

        }
        print( Request.objects.filter(author=request.user).count())
    return render(request, "desk/desk.html", context)


@login_required
def lazy_load_posts(request):
    firstData = Picture.objects.filter(
        Q(author__id__in=request.user.following.all()) | Q(author=request.user))
    secondData = Request.objects.filter(Q(author__id__in=request.user.following.all()) | Q(author=request.user))
    posts = sorted(
        chain(firstData, secondData),
        key=attrgetter('createdAdd'), reverse=True)
    page = request.POST.get('page')
    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = 5
    paginator = Paginator(posts, results_per_page)
    try:
        posts = paginator.page(int(page))
    except PageNotAnInteger:
        posts = paginator.page(2)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # build a html posts list with the paginated posts
    posts_html = loader.render_to_string(
        'registration/posts.html',
        {'posts': posts,
         "request": request}
    )
    # package output data and return it as a JSON object
    output_data = {
        'posts_html': posts_html,
        'has_next': posts.has_next()
    }
    return JsonResponse(output_data)


@login_required
def picture(request):
    if request.method == 'POST':
        try:
            flag = request.POST.get("flag")
            deletename = Picture.objects.get(pk=flag, author=request.user)
            deletename.delete()
        except:
            pass
        request.POST._mutable = True
        request.POST.update({"author": request.user, "status": "p"})
        request.POST._mutable = False
        f = PictureForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            return redirect("/account/")
        else:
            print("invalid")

    return redirect("/account/")


@login_required
def follow(request, username=None):
    if request.method == 'POST':
        # print(request.POST["follow"])
        try:
            follow = request.POST.get("follow")
            if follow != request.user :
                UserStart = User.objects.get(username=follow)
                request.user.following.add(UserStart)
                UserStart.followers.add(request.user)
                notificationAdd(receiver=UserStart, title="شما را دنبال کرد", url=f"/p/{request.user.username}/"
                                , user=request.user)
        except:
            unfollow = request.POST.get("unfollow")
            UserStart = User.objects.get(username=unfollow)
            request.user.following.remove(UserStart)
            UserStart.followers.remove(request.user)

    if username:
        UserStart = User.objects.get(username=username)
        request.user.following.add(UserStart)
        UserStart.followers.add(request.user)
        notificationAdd(receiver=UserStart, title="شما را دنبال کرد", url=f"/p/{request.user.username}/"
                        , user=request.user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')


@login_required
def addPicture(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"author": request.user, "status": "p"})
        request.POST._mutable = False
        f = PictureForm(request.POST, request.FILES)
        print(request.POST)
        if f.is_valid():
            f.save()
            context = {
                "form": PictureForm(),
            }
            return redirect("/account/")
    context = {
        'form': PictureForm(),
        "sucsess": False,
    }
    return render(request, "registration/addPicture.html", context)


@login_required
def addCv(request):
    if request.method == 'POST':
        try:
            start = request.POST.get("start")
            end = request.POST.get("end")
            start = jalaliConvertToGregorian(start.split("/"))
            start = datetime.date(start[0], start[1], start[2])
            end = jalaliConvertToGregorian(end.split("/"))
            end = datetime.date(end[0], end[1], end[2])
            request.POST._mutable = True
            request.POST.update({"person": request.user, 'start': start, 'end': end})
            request.POST._mutable = False
        except:
            request.POST._mutable = True
            request.POST.update({"person": request.user})
            request.POST._mutable = False

        f = TimelineForm(request.POST)
        if f.is_valid():
            f.save()
            context = {
                "form": TimelineForm(),
            }
            return redirect(f"/p/{request.user.username}/cv")
    context = {
        'form': TimelineForm(),
    }
    return render(request, "registration/addCv.html", context)


@login_required
def addService(request):
    if request.method == 'POST':
        if request.POST.get("nameProduct") == "" and request.POST.get("specialName") == "":
            return redirect(request.META.get('HTTP_REFERER'))
        request.POST._mutable = True
        request.POST.update({"author": request.user})
        request.POST._mutable = False
        # f = ServiceForm(request.POST)
        f = ''
        if f.is_valid():
            f.save()
            context = {
                # "form": ServiceForm(),
            }
            return redirect(f"/p/{request.user.username}/service")
    context = {
        # 'form': ServiceForm(),
    }
    return render(request, "registration/addService.html", context)


@login_required()
def addRequest(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"author": request.user})
        request.POST._mutable = False
        f = RequestForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect(f"/p/{request.user.username}/")
    context = {
        'form': RequestForm(),
    }
    return render(request, "registration/addRequest.html", context)


@login_required
def addAcceptRequest(request, pk):
    requestInstanse = Request.objects.get(pk=pk)
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"author": request.user})
        request.POST._mutable = False
        f = AcceptForm(request.POST)
        print(f.errors)
        if f.is_valid():
            newForm = f.save()
            requestInstanse.subcategories.add(newForm)
            requestInstanse.save()
            return redirect(f"/request/{pk}/")
    context = {
        'form': AcceptForm(),
    }
    return render(request, "registration/addAcceptRequest.html", context)


@login_required
def addSafePayment(request, username):
    receiver = User.objects.get(username=username)
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"sender": request.user, "senderBoolean": False, "paymentBoolean": False,
                             "receiver": receiver})
        request.POST._mutable = False
        price = request.POST.get("price")

        if int(price) > request.user.cash:
            return redirect(f"/wallet/IncreaseMoney/{int(price) - request.user.cash}/")
        else:
            userCashChanging = request.user
            userCashChanging.cash -= price
            userCashChanging.save()
        f = SafePaymentForm(request.POST)
        if f.is_valid():
            forSafePaymentAddTrello = f.save()
            safePaymentAddTrello(forSafePaymentAddTrello)
            context = {
                "form": SafePaymentForm(),
            }
            notificationAdd(receiver=receiver, title="پرداخت امن جدیدی از طریق این کاربر برای شما فعال شد",
                            url='/account/listSafePayment/', user=request.user)

            notificationAdd(receiver=request.user, title="پرداخت امن شما برای این کاربر فعال شد",
                            url='/account/listSafePayment/', user=receiver)

            try:
                send_mail(
                    'پرداخت امن',
                    f"پرداخت امن جدیدی از طریق {request.user.get_full_name} برای شما فعال شد",
                    'treaget@gmail.com',
                    [receiver.email],
                    fail_silently=False,
                )
            except Exception as e: print(e)
          
            return redirect(f"/p/{request.user.username}/")
    context = {
        'form': SafePaymentForm(),
    }
    return render(request, "registration/addSafePayment.html", context)


def addSafePaymentOrder(request, pk):
    orderData = OrderUser.objects.get(pk=pk)
    if request.user == orderData.author and request.user.cash >= orderData.price:
        UserInstance = request.user
        UserInstance.cash -= orderData.price
        UserInstance.save()
        SafePaymentInstance = SafePayment(price=orderData.price, description=orderData.body,
                                          receiver=orderData.designer, sender=orderData.author)
        SafePaymentInstance.save()
        safePaymentAddTrello(SafePaymentInstance)
        orderData.safePayment = SafePaymentInstance
        orderData.save()
        notificationAdd(receiver=orderData.designer, title="پرداخت امن جدیدی از طریق این کاربر برای شما فعال شد",
                        url='/account/listSafePayment/', user=orderData.author)
        notificationAdd(receiver=orderData.author, title="پرداخت امن شما برای این کاربر فعال شد",
                        url='/account/listSafePayment/', user=orderData.designer)
        try:
            send_mail(
                'پرداخت امن',
                f"پرداخت امن جدیدی از طرف {orderData.author.get_full_name} برای شما فعال شد",
                'treaget@gmail.com',
                [orderData.designer.email],
                fail_silently=False,
            )
        except Exception as e: print(e)
     
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(f"/wallet/IncreaseMoney/{int(orderData.price) - request.user.cash}/")


@login_required
def profile(request):
    obj = get_object_or_404(User, pk=request.user.pk)
    form = UserForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES or None, instance=obj)
        print("!")
        if form.is_valid():
            print("is valid before")
            form.save()
            print("is valid")
            form = UserForm(request.POST or None, instance=obj)
            context = {
                'form': form,
                "success": True,
            }
            return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'form': form,
        "success": False,
    }
    return render(request, "registration/setting.html", context)




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        userCheck = User.objects.filter(username=username).exists()
        emailCheck = User.objects.filter(email=email).exists()
        phoneCheck = User.objects.filter(phone_number=phone_number).exists()
        if userCheck:
            context = {
                'form': UserAddForm(),
                "success": "این کاربر از قبل وجود دارد",
            }
            return render(request, "registration/signup.html", context)
        elif emailCheck:
            context = {
                'form': UserAddForm(),
                "success": "کاربری از قبل اکانتی با این ایمیل ساخته است",
            }
            return render(request, "registration/signup.html", context)
        elif phoneCheck:
            context = {
                'form': UserAddForm(),
                "success": "کاربری از قبل اکانتی با این شماره تلفن ساخته است",
            }
            return render(request, "registration/signup.html", context)
        f = UserAddForm(request.POST)
        print(f.errors)
        if f.is_valid():
            if request.POST.get('ServiceProvider') == "true":
                ServiceProviderData = True
            elif request.POST.get('ServiceProvider') == "false":
                ServiceProviderData = False
            else:
                ServiceProviderData = None
            User.objects.create_user(first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'),
                                     email=request.POST.get('email'), username=request.POST.get('username').lower(),
                                     password=request.POST.get('password'), ServiceProvider=ServiceProviderData,phone_number=request.POST.get('phone_number'),verify_phone=False)
            userInstance = User.objects.get(username = request.POST.get('username').lower())
            try:
                send_mail(
                    'به سایت تریگت خوش آمدید',
                    f"سلام {userInstance.first_name} عزیز \nبه تریگت خوش آمدید لطفا قوانین و توضیحات سایت را مطالعه کنید در صورتی که به راهنمایی بیشتری نیاز داشتید با ما در ارتباط باشید . برای شما در تمام مراحل کاری در تریگت آرزوی موفقیت میکنیم \n https://treaget.com/Rules/  ",
                    'treaget@gmail.com',
                    [userInstance.email],
                    fail_silently=False,
                )
            except Exception as e: print(e)
            return redirect("/account/login/")
    context = {
        "page": "addpicture",
        'form': UserAddForm(),
        "sucsess": False,
    }
    return render(request, "registration/signup.html", context)





@login_required
def message(request, username=None):
    messages = Message.objects.filter(Q(author=request.user) | Q(receiver=request.user))
    userlist = []
    for message in messages:
        if message.receiver == request.user:
            userlist.append(message.author)
        elif message.author == request.user:
            userlist.append(message.receiver)
    if username == None:
        context = {
            'bodyClass': "vertical-layout vertical-menu-modern content-left-sidebar chat-application navbar-floating footer-static ",
            'conversations': deleteDuplicate(userlist),
            'is_user_chat': True

        }
        return render(request, "registration/message.html", context)
    else:
        userNotBe = None
        tester = True
        for item in deleteDuplicate(userlist):
            if item.username == username:
                tester = False
        if tester == True:
            userNotBe = User.objects.get(username=username)

        messages_User = Message.objects.filter(author=request.user,
                                               receiver=User.objects.get(username=username)) | Message.objects.filter(
            author=User.objects.get(username=username), receiver=request.user).order_by('pk')
        listMessage=[]
        for  message in messages_User:
            if message.receiver == request.user :
                message.read = True
                message.save()
            listMessage.append(message)
        context = {
            'bodyClass': "vertical-layout vertical-menu-modern content-left-sidebar chat-application navbar-floating footer-static ",
            'conversations': deleteDuplicate(userlist),
            'is_user_chat': True,
            'user_self': User.objects.get(username=username),
            "messages_User": listMessage,
            'userNotBe': userNotBe

        }
        return render(request, "registration/message.html", context)


@login_required
def LikePost(request):
    print(request.POST.get("id_mhs"))
    result = Picture.objects.get(pk=request.POST.get("id_mhs"))
    liked = False
    for userLike in result.like.all():
        if userLike == request.user:
            liked = True
            result.like.remove(request.user)
            request.user.like.remove(result)
            break
        else:
            liked = False
    if liked == False:
        result.like.add(request.user)
        request.user.like.add(result)
    return render(request, "registration/message.html")


def cv(request, slug):
    IP = User.objects.get(username=slug)

    if request.user.ip_address not in IP.numberVisitors.all():
        IP.numberVisitors.add(request.user.ip_address)
    categorySlice = []
    for result in Picture.objects.filter(author=User.objects.get(username=slug)):
        for re in result.category.all():
            categorySlice.append([re.title, re.pk])
    userResult = User.objects.get(username=slug)
    context = {

        "title": "استودیو سران",
        'user': userResult,
        # 'service': Service.objects.filter(author=User.objects.get(username=slug)).order_by('createdadd'),
        "cv": Timeline.objects.filter(person=User.objects.get(username=slug)).order_by('createdAdd')[::-1],
        'categorySlice': deleteDuplicate(categorySlice)

    }
    if userResult.ServiceProvider:
        context.update(
            {"picturesCount": Picture.objects.filter(author=User.objects.get(username=slug)).count})
    else:
        return HttpResponseNotFound("404")
    return render(request, "profile/cv.html", context)


def favourites(request, slug):
    IP = User.objects.get(username=slug)

    if request.user.ip_address not in IP.numberVisitors.all():
        IP.numberVisitors.add(request.user.ip_address)
    categorySlice = []
    for result in Picture.objects.filter(author=User.objects.get(username=slug)):
        for re in result.category.all():
            categorySlice.append([re.title, re.pk])
    userResult = User.objects.get(username=slug)
    if userResult.ServiceProvider:
        return HttpResponseNotFound("404")
    context = {
        'user': userResult,
        # 'service': Service.objects.filter(author=User.objects.get(username=slug)).order_by('createdadd'),
        'favourites': userResult.like.all().order_by('createdAdd')[0:20:],
        'categorySlice': deleteDuplicate(categorySlice)
    }
    return render(request, "profile/favourites.html", context)


def service(request, slug):
    IP = User.objects.get(username=slug)

    if request.user.ip_address not in IP.numberVisitors.all():
        IP.numberVisitors.add(request.user.ip_address)
    categorySlice = []
    for result in Picture.objects.filter(author=User.objects.get(username=slug)):
        for re in result.category.all():
            categorySlice.append([re.title, re.pk])
    userResult = User.objects.get(username=slug)
    context = {

        "title": "استودیو سران",
        'user': userResult,
        # 'service': Service.objects.filter(author=User.objects.get(username=slug)).order_by('createdadd'),
        # "cv": timeline.objects.filter(person=User.objects.get(username=slug)).order_by( 'createdadd')[::-1],
        'categorySlice': deleteDuplicate(categorySlice)

    }
    if userResult.ServiceProvider:
        context.update(
            {"picturesCount": Picture.objects.filter(author=User.objects.get(username=slug)).count})
    else:
        return HttpResponseNotFound("404")
    return render(request, "profile/service.html", context)


@login_required
def checkoutUser(request, slug, service=None):
    if request.method == "POST":
        request.POST._mutable = True
        if service:
            # serviceResult = Service.objects.get(pk=service)
            serviceResult = False
            if serviceResult.price:
                request.POST.update({"designer": User.objects.get(username=slug), "author": request.user,
                                    'service': serviceResult, 'price': serviceResult.price, 'accept': None})
            else:
                request.POST.update({"designer": User.objects.get(username=slug), "author": request.user,
                                    'service': serviceResult, 'accept': None})
        else:
            request.POST.update({"designer": User.objects.get(username=slug), "author": request.user, 'accept': None})
        request.POST._mutable = False
        f = OrderUserForm(request.POST)
        print(f.errors)
        if f.is_valid():
            f.save()
            notificationAdd(receiver=request.user, title="سفارش شما برای این کاربر ثبت شد", url='/account/orders/'
                            , user=User.objects.get(username=slug))
            notificationAdd(receiver=User.objects.get(username=slug), title="درخواست سفارش جدیدی برای شما ثبت کرد",
                            url='/account/orders/', user=request.user)
            try:
                send_mail(
                    "ثبت سفارش",
                    f"کاربر {request.user} درخواست سفارش جدیدی برای شما ثبت کرد",
                    'treaget@gmail.com',
                    [User.objects.get(username=slug).email],
                    fail_silently=False,
                )
            except Exception as e: print(e)
            return redirect('/account/notification/')
    context = {
        'form': OrderUserForm(),
        # "products": Products.objects.filter(status="p"),

    }
    if service:
        context.update({
            # 'service': Service.objects.get(pk=service),
        })
    return render(request, 'main/checkoutUser.html', context)


@login_required()
def deleteCv(request, pk):
    Timeline.objects.get(person=request.user, pk=pk).delete()
    return redirect(f"/p/{request.user.username}/cv")


@login_required()
def deleteService(request, pk):
    # Service.objects.get(author=request.user, pk=pk).delete()
    return redirect(f"/p/{request.user.username}/service")


@login_required()
def notification(request):
    result = Notification.objects.filter(receiver=request.user)
    for data in result:
        if data.readingStatus == False :
            data.readingStatus = True
            data.save()
    context = {
        'notifications': result
    }

    return render(request, "desk/notification.html", context)


@login_required()
def orders(request):
    context = {
        'orders': OrderUser.objects.filter(Q(designer=request.user) | Q(author=request.user)).order_by("-pk")
    }

    return render(request, "desk/orders.html", context)


@login_required()
def ordersTrue(request, pk):
    order = OrderUser.objects.get(pk=pk)
    order.accept = True
    order.save()

    return redirect("/account/orders/")


@login_required()
def ordersFalse(request, pk):
    order = OrderUser.objects.get(pk=pk)
    order.accept = False
    order.save()

    return redirect("/account/orders/")


@login_required()
def SafePaymentAccept(request, pk):
    safePaymentResult = SafePayment.objects.get(pk=pk)
    if request.user == safePaymentResult.sender:
        if safePaymentResult.paymentBoolean:
            userResult = safePaymentResult.receiver
            userResult.cash += safePaymentResult.price
            userResult.save()
        safePaymentResult.senderBoolean = True
        safePaymentResult.save()

    elif request.user == safePaymentResult.receiver:
        if safePaymentResult.senderBoolean:
            userResult = safePaymentResult.receiver
            userResult.cash += safePaymentResult.price
            userResult.save()
        safePaymentResult.paymentBoolean = True
        safePaymentResult.save()

    return redirect("/account/desk/")


@login_required()
def SafePaymentRefuse(request, pk):
    safePaymentResult = SafePayment.objects.get(pk=pk)

    if request.user == safePaymentResult.receiver:
        if safePaymentResult.senderBoolean is False and safePaymentResult.paymentBoolean is not None:
            userResult = safePaymentResult.sender
            userResult.cash += safePaymentResult.price
            userResult.save()
            safePaymentResult.paymentBoolean = None
            safePaymentResult.save()

    return redirect("/account/desk/")


@login_required()
def listSafePayment(request):
    context = {
        'SafePayment': SafePayment.objects.filter(Q(receiver=request.user) | Q(sender=request.user)).order_by("-pk")
    }
    return render(request, "desk/listSafePayment.html", context)


@login_required()
def addDispute(request, pk):
    form = DisputeForm(request.POST)
    resultSafePayment = SafePayment.objects.get(pk=pk)
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"author": request.user, 'safePayment': resultSafePayment})
        request.POST._mutable = False

        if form.is_valid():
            form.save()
            return redirect("/account/listDispute")
    context = {
        'form': DisputeForm(),
        "success": False,
    }
    return render(request, "registration/addDispute.html", context)


@login_required()
def listDispute(request):
    context = {
        'Dispute': Dispute.objects.filter(author=request.user),
    }
    return render(request, "desk/listDispute.html", context)


@login_required()
def createSafePayment(request, pk_request, pk_accept):
    InstanceRequest = Request.objects.get(pk=pk_request)
    AcceptInstanse = Accept.objects.get(pk=pk_accept)
    if request.user.cash >= InstanceRequest.price:
        cashUser = request.user
        cashUser.cash -= InstanceRequest.price
        cashUser.save()
        safePaymentInstanse = SafePayment(price=InstanceRequest.price, sender=request.user,
                                          description=InstanceRequest.title, receiver=AcceptInstanse.author)
        safePaymentInstanse.save()
        redirect("/account/listSafePayment")
    else:
        return redirect(f"/wallet/IncreaseMoney/{int(InstanceRequest.price) - request.user.cash}/")

    # TODO : write else


@login_required()
def projectManagement(request, pk):
    context = {
        'Trello': Trello.objects.filter(forSafePayment=SafePayment.objects.get(pk=pk)),
        "SafePayment": SafePayment.objects.get(pk=pk)
    }
    return render(request, "registration/Trello.html", context)


@login_required()
def AddProjectManagement(request, pk):
    forSafePayment = SafePayment.objects.get(pk=pk)
    if request.method == 'POST' and forSafePayment.receiver == request.user:
        request.POST._mutable = True
        request.POST.update({"forSafePayment": forSafePayment})
        request.POST._mutable = False
        form = TrelloForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

    return redirect(f"/account/projectManagement/{forSafePayment.pk}/")


@login_required()
def AddSubsetProjectManagement(request, pk):
    forTrello = Trello.objects.get(pk=pk)
    if request.method == 'POST' and forTrello.forSafePayment.receiver == request.user:
        request.POST._mutable = True
        request.POST.update({"author": request.user})
        request.POST._mutable = False
        form = SubsetTrelloForm(request.POST)
        print(form.errors)
        if form.is_valid():
            valueForm = form.save()
            forTrello.subsetTrello.add(valueForm)

    return redirect(f"/account/projectManagement/{forTrello.forSafePayment.pk}/")


@login_required()
def deleteSubsetTrello(request, pk):
    InstanceSubsetTrello = SubsetTrello.objects.get(pk=pk)
    if InstanceSubsetTrello.author == request.user:
        InstanceSubsetTrello.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def deleteTrello(request, pk):
    InstanceTrello = Trello.objects.get(pk=pk)
    if InstanceTrello.forSafePayment.receiver == request.user:
        InstanceTrello.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def numberOfFollowers(request, username):
    context = {
        "results": User.objects.get(username=username).followers.all()
    }
    return render(request, "registration/FollowersNumber.html", context)


def numberOfFollowing(request, username):
    context = {
        "results": User.objects.get(username=username).following.all()
    }
    return render(request, "registration/FollowersNumber.html", context)
