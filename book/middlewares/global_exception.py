from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class GlobalExceptionHandle(MiddlewareMixin):
    def process_exception(self, request, exception):
        """视图函数发生异常时调用"""
        print('----process_exception1----')

        return render(request, 'layout/404.html', locals())
