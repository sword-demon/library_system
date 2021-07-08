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
    path('', views.index, name='home'),
    path('reg/', views.reg, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('publish/', views.publish, name='publish'),
    path('author/', views.author, name='author'),
    path('add/', views.add, name='add'),
    path('author/<int:id>/ownbooks/', views.author_books, name='author_own_book'),
    path('book/<int:id>/edit/', views.book_edit, name="edit_book"),
    path('book/delete/', views.book_delete, name="delete_book"),
]
