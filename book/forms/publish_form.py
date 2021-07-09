from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError


class AddPublish(forms.Form):
    name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "出版社名称至少3个字符",
            "required": "出版社名称不能为空"
        }
    )
    city = forms.CharField(
        required=True,
        error_messages={
            "required": "城市不能为空"
        }
    )
    email = forms.EmailField(required=True, error_messages={"required": "邮箱不能为空"})


class UpdatePublish(forms.Form):
    id = forms.IntegerField(required=True, error_messages={"required": "编辑参数不能为空"})
    name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "出版社名称至少3个字符",
            "required": "出版社名称不能为空"
        }
    )
    city = forms.CharField(
        required=True,
        error_messages={
            "required": "城市不能为空"
        }
    )
    email = forms.EmailField(required=True, error_messages={"required": "邮箱不能为空"})
