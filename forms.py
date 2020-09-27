# coding:utf8
# @Time : 2020/7/2 上午1:26
# @Author : Erics
# @File : forms.py
# @Software: PyCharm
from flask_wtf import FlaskForm  # pip install flask_wtf -i https://mirrors.aliyun.com/pypi/simple
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from models import User, Cate
from flask import session


class RegisterForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('账号不能为空！'),
            Length(max=16, message='账号不大于%(max)d位！')
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            "placeholder": "请输入账号！",
            'maxlength': '16',
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！"),
            Length(min=6, max=20, message='密码长度必须大于%(min)d不少于%(max)d位！')
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            'maxlength': '20',
            'minlength': '6',
        }
    )
    re_pwd = PasswordField(
        label=u"确认密码",
        validators=[
            DataRequired("确认密码不能为空！"),
            Length(min=6, max=20, message='密码长度必须大于%(min)d不少于%(max)d位!'),
            EqualTo('pwd', message="两次输入密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码！",
            'maxlength': '20',
            'minlength': '6',
        }
    )
    verification_code = StringField(
        label="验证码",
        validators=[
            DataRequired("验证码不能为空！"),
            Length(min=4, max=4, message='请输入%(max)d位验证码！'),
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码！",
            'maxlength': '4',
            'minlength': '4',
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    # 自定义字段验证规则：validate_字段名
    # 自定义账号验证功能：账号是否已经存在
    def validate_name(self, field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count > 0:
            raise ValidationError("账号已存在，不能重复注册！")

    # 自定义验证码验证功能：验证码是否正确

    def validate_verification_code(self, field):
        code = field.data  # 4j28
        if session.get("code") and session.get("code").lower() != code.lower():
            raise ValidationError("验证码不正确！")


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('账号不能为空！'),
            Length(max=16, message='账号不大于%(max)d位！')
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            "placeholder": "请输入账号！",
            'maxlength': '16',
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空！"),
            Length(min=6, max=20, message='密码长度必须大于%(min)d不少于%(max)d位！')
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            'maxlength': '20',
            'minlength': '6',
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class ArticleAddForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAddForm, self).__init__(*args, **kwargs)
        cate = Cate.query.all()  # [<Cate 2>, <Cate 1>]
        self.cate_id.choices = [(i.id, i.title) for i in cate]
        self.cate_id.choices.reverse()
        # print(self.cate_id.choices)  # [(1, '科技'), (2, '社会')]

    title = StringField(
        label='标题',
        description='标题',
        validators=[
            DataRequired('标题不能为空！'),
            Length(max=30, message='标题长度不应该大于%(max)d位！')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入标题',
            'maxlength': '30'
        }
    )
    cate_id = SelectField(
        label='分类',
        description='分类',
        validators=[
            DataRequired('分类不能为空！'),
        ],
        choices=None,
        default=1,
        coerce=int,
        render_kw={
            'class': 'form-control'
        }
    )

    logo = FileField(
        label='封面',
        description='封面',
        validators=[
            DataRequired('封面不能为空！')
        ],
        render_kw={
            'class': 'form-control-static'
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空！"),
            Length(max=2000, message='不得超过%(max)d字')
        ],
        description="内容",
        render_kw={
            "style": "height:300px;",
            "id": "content"
        }
    )
    submit = SubmitField(
        "发布",
        render_kw={
            "class": "btn btn-danger",
        }
    )


class ArticleEditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        cate = Cate.query.all()  # [<Cate 2>, <Cate 1>]
        self.cate_id.choices = [(i.id, i.title) for i in cate]
        self.cate_id.choices.reverse()
        # print(self.cate_id.choices)  # [(1, '科技'), (2, '社会')]

    title = StringField(
        label='标题',
        description='标题',
        validators=[
            DataRequired('标题不能为空！'),
            Length(max=30, message='标题长度不应该大于%(max)d位！')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入标题',
            'maxlength': '30'
        }
    )
    cate_id = SelectField(
        label='分类',
        description='分类',
        validators=[
            DataRequired('分类不能为空！'),
        ],
        choices=None,
        default=1,
        coerce=int,
        render_kw={
            'class': 'form-control'
        }
    )

    logo = FileField(
        label='封面',
        description='封面',
        validators=[
            DataRequired('封面不能为空！')
        ],
        render_kw={
            'class': 'form-control-static'
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空！"),
            Length(max=2000, message='不得超过%(max)d字')
        ],
        description="内容",
        render_kw={
            "style": "height:300px;",
            "id": "content"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )
