from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

# Create your views here.
from book.forms.author_form import AddAuthor, UpdateAuthor
from book.forms.book_form import UpdateBook, AddBook
from book.forms.publish_form import AddPublish, UpdatePublish
from book.forms.user_form import RegisterForm, LoginForm
from book.models import UserInfo, Book, Publish, Author
from utils.json_response import Show
from utils.page import ShowPage
from utils.ajax_login_required import check_login

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
    publishes = Publish.objects.all()
    authors = Author.objects.all()

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


@login_required
def add(request):
    if request.method == "POST":
        book_form = AddBook(request.POST)
        author_id_list = request.POST.getlist("author_id_list")
        book_obj = Book.objects.filter(title=request.POST.get("title")).exists()
        if book_obj:
            return Show.fail("该书已存在")
        if book_form.is_valid():
            try:
                book = Book.objects.create(**book_form.cleaned_data)
                if book:
                    book.authors.add(*author_id_list)
                    return Show.success("添加成功")
                else:
                    return Show.fail("数据库异常，请稍后重试!")
            except Exception as e:
                print("异常: %s" % str(e))
                return Show.fail("网络错误，请等会重试!")
        else:
            return Show.fail(book_form.errors)

    publishes = Publish.objects.all().values("id", "name")
    authors = Author.objects.all().values("id", "name")
    return render(request, 'root/add.html', locals())


@check_login
def update_book(request):
    if request.method == "POST":
        book_form = UpdateBook(request.POST)
        print(request.POST)
        author_id_list = request.POST.getlist("author_id_list")
        print(author_id_list)
        if book_form.is_valid():
            try:
                edit_book_obj = Book.objects.filter(id=request.POST.get("id")).first()
                print(edit_book_obj)
                Book.objects.filter(id=request.POST.get("id")).update(
                    **book_form.cleaned_data)
                edit_book_obj.authors.set(author_id_list)
                return Show.success("修改成功")
            except Exception as e:
                print(str(e))
                return Show.fail("网络异常，请稍后再试!")
        else:
            print(book_form.errors)
            return Show.fail(book_form.errors)
    else:
        return Show.fail("非法请求")


@check_login
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


@login_required
def add_author(request):
    if request.method == "POST":
        author_form = AddAuthor(request.POST)
        if author_form.is_valid():
            Author.objects.create(**author_form.cleaned_data)
            return Show.success("添加成功")
        else:
            return Show.fail(author_form.errors)
    return render(request, 'author/add.html', locals())


@check_login
def update_author(request):
    if request.method == "POST":
        author_form = UpdateAuthor(request.POST)
        if author_form.is_valid():
            author_obj = Author.objects.filter(id=request.POST.get("id")).update(
                **author_form.cleaned_data)
            if author_obj:
                return Show.success("修改成功")
            else:
                return Show.fail("该数据不存在")
        else:
            return Show.fail(author_form.errors)
    else:
        return Show.fail("非法请求")


@check_login
def delete_author(request):
    if request.method != "POST":
        return Show.fail("请求方法错误")

    author_id = request.POST.get("id")
    if author_id is None:
        return Show.fail("参数错误")
    try:
        Publish.objects.filter(pk=author_id).first().delete()
        return Show.success("删除成功")
    except Exception as e:
        print("异常: %s" % str(e))
        return Show.fail("网络异常,请稍后重试")


def author_books(request, id):
    """
    查询作者下有多少书籍
    :param request:
    :param id:
    :return:
    """
    if id is None:
        return render(request, 'layout/500.html')
    id = int(id)
    author = Author.objects.filter(id=id).first()
    if author is None:
        return render(request, 'author/author_books.html', {'errors': '作者不存在'})
    books = author.book_set.all()
    return render(request, 'author/author_books.html', {'books': books, 'author': author})


def publish_books(request, id):
    """
    查看该出版社下的出版的书籍
    :param request:
    :param id:
    :return:
    """
    if id is None:
        return render(request, 'layout/500.html')
    publish = Publish.objects.filter(id=id).first()
    books = publish.book_set.all()
    return render(request, 'publish/publish_books.html', {'books': books, 'publish': publish})


@login_required
def add_publish(request):
    if request.method == "POST":
        publish_form = AddPublish(request.POST)
        if publish_form.is_valid():
            # print(publish_form.cleaned_data)
            Publish.objects.create(**publish_form.cleaned_data)
            return Show.success("添加成功")
        else:
            return Show.fail(publish_form.errors)
    return render(request, 'publish/add.html', locals())


@check_login
def update_publish(request):
    if request.method == "POST":
        publish_form = UpdatePublish(request.POST)
        if publish_form.is_valid():
            # print(publish_form.cleaned_data)
            publish_obj = Publish.objects.filter(id=request.POST.get("id")).update(
                **publish_form.cleaned_data)
            if publish_obj:
                return Show.success("修改成功")
            else:
                return Show.fail("该数据不存在")
        else:
            return Show.fail(publish_form.errors)
    else:
        return Show.fail("非法请求")


@check_login
def delete_publish(request):
    if request.method != "POST":
        return Show.fail("请求方法错误")

    publish_id = request.POST.get("id")
    if publish_id is None:
        return Show.fail("参数错误")
    try:
        Publish.objects.filter(pk=publish_id).first().delete()
        return Show.success("删除成功")
    except Exception as e:
        print("异常: %s" % str(e))
        return Show.fail("网络异常,请稍后重试")
