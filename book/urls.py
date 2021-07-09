"""library_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from book import views

urlpatterns = [
    # 首页
    path('', views.index, name='home'),
    # 注册
    path('reg/', views.reg, name='register'),
    # 登录
    path('login/', views.login, name='login'),
    # 退出
    path('logout/', views.logout, name='logout'),
    # 出版社列表
    path('publish/', views.publish, name='publish'),
    # 作者列表
    path('author/', views.author, name='author'),
    # 添加书籍
    path('add/', views.add, name='add'),
    # 查看作者拥有的书籍
    path('author/<int:id>/ownbooks/', views.author_books, name='author_own_book'),
    # 编辑书籍
    path('book/<int:id>/edit/', views.book_edit, name="edit_book"),
    # 删除书籍
    path('book/delete/', views.book_delete, name="delete_book"),
    # 添加出版社
    path('add_publish/', views.add_publish, name='add_publish'),
    # 更新出版社信息
    path('update_publish/', views.update_publish, name='update_publish'),
    # 删除出版社
    path('publish/delete/', views.delete_publish, name='delete_publish'),
    # 添加作者
    path('add_author/', views.add_author, name='add_author'),
    # 更新作者信息
    path('update_author/', views.update_author, name='update_author'),
    # 删除作者
    path('author/delete/', views.delete_author, name='delete_author'),
]
