from django import forms


class AddAuthor(forms.Form):
    name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "作者名称至少3个字符",
            "required": "作者名称不能为空"
        }
    )
    age = forms.IntegerField(
        required=True,
        error_messages={
            "required": "年龄不能为空"
        }
    )
    mobile = forms.CharField(required=True, max_length=11,
                             error_messages={"required": "邮箱不能为空", "max_length": "手机号码最长11位"})
    birthday = forms.DateTimeField(required=True, error_messages={"required": "生日不能为空"})
    desc = forms.CharField(required=False)


class UpdateAuthor(forms.Form):
    id = forms.IntegerField(required=True, error_messages={"required": "编辑参数不能为空"})
    name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "作者名称至少3个字符",
            "required": "作者名称不能为空"
        }
    )
    age = forms.IntegerField(
        required=True,
        error_messages={
            "required": "年龄不能为空"
        }
    )
    mobile = forms.CharField(required=True, max_length=11,
                             error_messages={"required": "邮箱不能为空", "max_length": "手机号码最长11位"})
    birthday = forms.DateTimeField(required=True, error_messages={"required": "生日不能为空"})
    desc = forms.CharField(required=False)
