from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

# Create your views here.
from book.forms.user_form import RegisterForm, LoginForm
from book.models import UserInfo, Book, Publish, Author
from utils.json_response import Show
from utils.page import ShowPage

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage

import logging
from library_system import settings


def index(request):
    # 显示所有的图书
    page = int(request.GET.get("page", 1))

    # 书籍总数
    total_count = Book.objects.all().count()

    page_obj = ShowPage(page, total_count, per_page=settings.PER_PAGE, url_prefix="/book/", max_page=11, )
    books = Book.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()
    return render(request, 'root/index.html', locals())


def reg(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            try:
                user = UserInfo.objects.create_user(username=form.cleaned_data.get("username"),
                                                    password=form.cleaned_data.get("password"))
                if user:
                    return Show.success("注册成功，前去登录!")
                else:
                    return Show.fail()
            except Exception as e:
                print(str(e))
                logging.error(str(e))
                return Show.fail()
        else:
            return Show.fail(form.errors)

    form = RegisterForm()
    return render(request, 'auth/register.html', locals())


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
            if user is not None:
                auth.login(request, user)
                return Show.success("登录成功")
            else:
                return Show.fail("用户名或密码错误")
        else:
            return Show.fail(form.errors)
    form = LoginForm()
    return render(request, 'auth/login.html', locals())


def logout(request):
    """
    退出
    :param request:
    :return:
    """

    request.session.flush()

    return redirect("login")


def add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        pub_date = request.POST.get("pub_date")
        price = request.POST.get("price")
        publish_id = request.POST.get("publish_id")
        author_id_list = request.POST.getlist("author_id_list")
        try:
            book = Book.objects.create(title=title, pub_date=pub_date, price=price, publish_id=publish_id)
            if book:
                book.authors.add(*author_id_list)
                return Show.success("添加成功")
            else:
                return Show.fail("数据库异常，请稍后重试!")
        except Exception as e:
            print("异常: %s" % str(e))
            return Show.fail("网络错误，请等会重试!")

    publishes = Publish.objects.all().values("id", "name")
    authors = Author.objects.all().values("id", "name")
    return render(request, 'root/add.html', locals())


def book_edit(request, book_id):
    if request.method == "POST":
        pass
    book_info = Book.objects.filter(pk=book_id).first()
    return render(request, 'root/edit.html', locals())


def book_delete(request):
    if request.method != "POST":
        return Show.fail("请求类型错误")
    book_id = request.POST.get("id")
    if book_id is None:
        return Show.fail("参数错误")
    print(book_id)
    try:
        Book.objects.filter(id=book_id).first().delete()
        return Show.success("删除成功")
    except Exception as e:
        print("异常: %s" % str(e))
        return Show.fail("删除失败，网络异常，请稍后重试")


def publish(request):
    page = int(request.GET.get("page", 1))

    # 出版社总数
    total_count = Publish.objects.all().count()

    page_obj = ShowPage(page, total_count, per_page=settings.PER_PAGE, url_prefix="/book/publish/", max_page=11, )
    publishes = Publish.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()
    return render(request, 'publish/index.html', locals())


def author(request):
    page = int(request.GET.get("page", 1))

    # 出版社总数
    total_count = Author.objects.all().count()

    page_obj = ShowPage(page, total_count, per_page=settings.PER_PAGE, url_prefix="/book/author/", max_page=11, )
    authors = Author.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()
    return render(request, 'author/index.html', locals())


def author_books(request):
    pass
