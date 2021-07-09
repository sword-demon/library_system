from django import forms


class AddBook(forms.Form):
    title = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "书籍名称至少3个字符",
            "required": "书籍名称不能为空"
        }
    )
    pub_date = forms.DateTimeField(
        required=True,
        error_messages={
            "required": "出版日期不能为空"
        }
    )
    price = forms.DecimalField(required=True,
                               error_messages={"required": "价格不能为空"})
    publish_id = forms.IntegerField(required=True, error_messages={"required": "出版社为空"})


class UpdateBook(forms.Form):
    id = forms.IntegerField(required=True, error_messages={"required": "编辑参数不能为空"})
    title = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            "min_length": "书籍名称至少3个字符",
            "required": "书籍名称不能为空"
        }
    )
    pub_date = forms.DateTimeField(
        required=True,
        error_messages={
            "required": "出版日期不能为空"
        }
    )
    price = forms.DecimalField(required=True,
                               error_messages={"required": "价格不能为空"})
    publish_id = forms.IntegerField(required=True, error_messages={"required": "出版社为空"})
