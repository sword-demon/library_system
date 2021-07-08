from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from library_system import settings


class AuthCheck(MiddlewareMixin):
    def process_request(self, request):
        white_list = settings.WHITE_LIST

        if request.path in white_list:
            return None

        if request.user.username is not None:
            return redirect("login")
