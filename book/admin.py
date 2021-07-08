from django.contrib import admin

# Register your models here.
from book.models import Book, Author, Publish, UserInfo

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publish)
admin.site.register(UserInfo)
