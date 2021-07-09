from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class Author(models.Model):
    """作者表"""
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    mobile = models.CharField(max_length=11, unique=True)
    birthday = models.DateTimeField()
    desc = models.TextField()

    def __str__(self):
        return self.name

    def show_desc(self):
        if len(self.desc) > 30:
            return '{}......'.format(str(self.desc))[0:30]
        else:
            return str(self.desc)

    show_desc.allow_tags = True


class Publish(models.Model):
    """出版社表"""
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Book(models.Model):
    """书籍表"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, unique=True)
    pub_date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publish = models.ForeignKey(to=Publish, to_field="id", on_delete=models.CASCADE)  # 一对多

    authors = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print("模型校验没通过: %s" % e.message_dict)


class UserInfo(AbstractUser):
    """扩展用户表"""
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username
