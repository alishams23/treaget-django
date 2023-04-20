from itertools import count
from PIL.Image import Image
from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms.models import InlineForeignKeyField
from django.http.response import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.shortcuts import render, get_object_or_404
from .models import PostTag, Picture, Price, contact, BuyStudio, OrderUser, FAQ, Blog, Request, Rules, \
    Category

from profile_items.models import Services
from .forms import PostFormContact, ProductFormContact, OrderUserForm
from account.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Count
from random import randint


def index(request):
    if request.user.username:
        return redirect("/account/")
    context = {

        "title": "سران بازار",
        "products": PostTag.objects.filter(status="p"),
        'FAQs': FAQ.objects.filter(TypeFAQ='m').order_by('position'),
        'users': User.objects.all().order_by('pk').reverse()[0:6:],
        'Blogs': Blog.objects.all()

    }
    return render(request, 'main/index.html', context)


def rules(request):
    context = {
        'Rules': Rules.objects.all()
    }
    return render(request, 'main/Rules.html', context)


def explore(request):
    context = {
        'image': Picture.objects.all().order_by("?")[0:15]
    }
    if request.user.username:
        suggestion = User.objects.filter(~Q(followers=request.user) & ~Q(image="")).order_by("?")[0:8]
        context.update({'suggestion': suggestion})
    return render(request, 'explore/explore.html', context)


def lazyLoadExplore(request):
    page = request.POST.get('page')
    posts = Picture.objects.all().order_by("?"),
    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = 20
    paginator = Paginator(posts[0], results_per_page)
    posts = paginator.page(1)
    # try:
    #     posts = paginator.page(int(page))
    # except PageNotAnInteger:
    #     posts = paginator.page(2)
    # except EmptyPage:
    #     posts = paginator.page(1)
    # build a html posts list with the paginated posts
    posts_html = loader.render_to_string(
        'explore/postsExplore.html',
        {'image': posts,
         "request": request}
    )
    # package output data and return it as a JSON object
    output_data = {
        'posts_html': posts_html,
        'has_next': posts.has_next()
    }
    return JsonResponse(output_data)


def Contact(request):
    if request.method == 'POST':
        f = PostFormContact(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'یک پیام جدید در بخش ارتباط با ما دارید')
            redirect("/contact/")

    context = {

        "title": "ارتباط با ما",
        "form": PostFormContact(),
        "sucsess": False,
        "products": PostTag.objects.filter(status="p")

    }
    return render(request, 'main/contact.html', context)




def BuyStudioR(request, slug, price, mainprice, typee):
    price = price.strip().replace('_', ' ')
    ProductCategory = PostTag.objects.get(slug=slug)
    Productperices = ProductCategory.category.all()

    if request.method == 'POST':

        request.POST._mutable = True
        request.POST.update({"type1": slug, "type2": price, "type3": mainprice, "type4": typee})
        request.POST._mutable = False
        print(request.POST)
        f = ProductFormContact(request.POST, request.FILES)
        if f.is_valid():
            f.save()

            contex = {
                "object": get_object_or_404(PostTag, slug=slug, status="p"),
                "allbum": Picture.objects.filter(category=ProductCategory.id),
                "price": price,
                "PriceTipe": typee,
                "products": PostTag.objects.filter(slug=slug),
                "form": ProductFormContact(),
                "mainprice": mainprice,
                "sucsess": True, }
            return render(request, 'main/checkout.html', contex)

    else:

        contex = {
            "object": get_object_or_404(PostTag, slug=slug, status="p"),
            "allbum": Picture.objects.filter(category=ProductCategory.id),
            "price": price,
            "PriceTipe": typee,
            "products": PostTag.objects.filter(status="p"),
            "form": ProductFormContact(),
            "mainprice": mainprice,
            "sucsess": False,
        }
        return render(request, 'main/checkout.html', contex)


def deleteDuplicate(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)

    return res


def profile(request, slug):
    userResult = User.objects.get(username=slug)
    counter = 1
    for category in userResult.category.all() :
        if category.position == 0 :
            counter = 0
    if len(userResult.category.all()) == 0 :
        counter = 0
    if counter == 1 : return redirect(f"/p/{userResult.username}/cv")
    if request.user.ip_address not in userResult.numberVisitors.all():
        userResult.numberVisitors.add(request.user.ip_address)
    categorySlice = []
    for result in Picture.objects.filter(author=User.objects.get(username=slug)):
        for re in result.category.all():
            categorySlice.append([re.title, re.pk])
    context = {
        "title": "استودیو سران",
        'user': userResult,
        'Services': Services.objects.filter(author=User.objects.get(username=slug)).order_by('createdadd'),
        'categorySlice': deleteDuplicate(categorySlice)

    }
    if userResult.ServiceProvider:
        context.update(
            {"pictures": Picture.objects.filter(author=User.objects.get(username=slug)).order_by('createdAdd')[::-1],
             "picturesCount": Picture.objects.filter(author=User.objects.get(username=slug)).count})
    else:
        context.update({'RequestServices': Request.objects.filter(author=userResult)})
    return render(request, 'profile/profile.html', context)


def search(request):
    context = {
        # 'result': User.objects.filter(search=SearchVector('username_text__search', )).filter(search='ali'),
        'productsSearch': Category.objects.all(),
    }
    print(request.POST.get("category"))
    if request.method == 'POST':
        if "category" in request.POST and request.POST.get("category") != "":
            context.update({'results': User.objects.filter(
                Q(last_name__contains=request.POST.get("name")) | Q(first_name__contains=request.POST.get("name")) | Q(
                    username__contains=request.POST.get("name"))).filter(category__title__contains=request.
                                                                         POST.get("category")).distinct(), })
            print("1")
        else:
            context.update({'results': User.objects.filter(
                Q(last_name__contains=request.POST.get("name")) | Q(first_name__contains=request.POST.get("name")) | Q(
                    username__contains=request.POST.get("name"))).distinct(), })
            print("2")
        print(User.objects.filter(
            Q(last_name__contains=request.POST.get("name")) | Q(first_name__contains=request.POST.get("name")) | Q(
                username__contains=request.POST.get("name"))).distinct())

    return render(request, 'search/search.html', context)






def requestUser(request, pk):
    validation_user = True
    data = Request.objects.get(pk=pk)
    for accept in  data.subcategories.all():
        if accept.author == request.user :
            validation_user = False
    context = {
        'result': data,
        'validation_user':validation_user
    }
    return render(request, "main/request.html", context)
