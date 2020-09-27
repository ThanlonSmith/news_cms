# coding:utf8
# @Time : 2020/7/2 上午1:25
# @Author : Erics
# @File : views.py
# @Software: PyCharm
from flask import render_template, redirect, flash, session, Response, request, url_for
from forms import RegisterForm, LoginForm, ArticleAddForm, ArticleEditForm
from models import User, db, Article, Cate
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from create_app import app
from codes import Codes
from werkzeug.utils import secure_filename
import uuid
from functools import wraps

app.config["SECRET_KEY"] = "12345678"
app.config["UP"] = os.path.join(os.path.dirname(__file__), "static/images/uploads/")


def user_login_decorator(foo):
    @wraps(foo)
    def user_login(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login', next=request.url))
        return foo(*args, **kwargs)

    return user_login


# 获取验证码
@app.route("/codes/", methods=["GET"])
def codes():
    c = Codes()
    info = c.create_code()  # info：{'img_name': image_name, 'code': chars}
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    """
    print(__file__) # /media/thanlon/存储盘/项目实施/开发/Flask/article_cms/views.py
    print(os.path.dirname(__file__))  # /media/thanlon/存储盘/项目实施/开发/Flask/article_cms
    print(os.path.join('1', '2', '3'))  # 1/2/3
    print(image)  # /media/thanlon/存储盘/项目实施/开发/Flask/article_cms/static/code/b8009fbaf8774adca4c6b1747b4f1f12.jpg
    """
    with open(image, mode='rb') as f:
        image = f.read()
    session["code"] = info["code"]
    return Response(image, mimetype='jpeg')  # images:字节类型,mimetype告诉浏览器以何种方式打开


# 用户注册
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data  # 字典类型
        """
        print(data)  # {'name': 'thanlon', 'pwd': '123456', 're_pwd': '123456', 'verification_code': '4j28', 'submit': True, 'csrf_token': 'IjU1YTEwZDA3ZjQ5MTQ0NDM0MmM0MGVhNzMxMTJhZDNkMDQ0ODgwNDQi.XwH3wA.5SHm9PYdYZoiF8815FnRTcjfueo'}
        """
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            # pwd：pbkdf2:sha256:150000$VpYqRoBN$e2da700d98fea88e57a19c5943523301ff74a03a9869fff1e4fe16af3f59edc0
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录！", "ok")
        return redirect('/login/')
    return render_template("register.html", form=form)


# 登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user:
            # 安全起见登录时候不要提示没有用户名，直接提示用户或密码错误就可以了
            flash("用户或密码错误！", "error")
        else:
            # 校验成功返回True，失败返回False
            if not check_password_hash(user.pwd, data['pwd']):
                flash("用户或密码错误！", "error")
            else:
                session["id"] = user.id
                session["user"] = data["name"]
                flash(f"{session.get('user')}已成功登录，欢迎您的使用！", "ok")
                return redirect('/article/list/1/')
    return render_template("login.html", form=form)


# 退出登录
@app.route(rule='/logout/', methods=['GET'])
@user_login_decorator
def logout():
    session.pop('user', None)  # 如果没有key(user)返回None
    return redirect('/login/')  # 302跳转到登录页面


def change_name(name):
    """
    :param name: 2020-07-04_19-54.png
    :return: 新的文件名，时间格式字符串+唯一字符串+后缀名
    20200704214223bac609e7af8b48bc85d0514b8ae17907.png
    """
    info = os.path.splitext(name)
    """
    print('info：',info) # ('2020-07-04_19-54', '.png')
    """
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex + info[-1]


@app.route('/article/add/', methods=['GET', 'POST'])
@user_login_decorator
def article_add():
    form = ArticleAddForm()
    if form.validate_on_submit():
        data = form.data
        """
        print(data) # {'title': 'test', 'cate': 1, 'logo': <FileStorage: '2020-07-04_19-54.png' ('image/png')>, 'content': '<p>test</p>', 'submit': True, 'csrf_token': 'IjU1YTEwZDA3ZjQ5MTQ0NDM0MmM0MGVhNzMxMTJhZDNkMDQ0ODgwNDQi.XwCFIA.IP3Cg1BU5SkFcsuuQhffdp3kWok'}
        print(data['logo'] ) # <FileStorage: '2020-07-04_19-54.png' ('image/png')>
        print(form.logo,type(form.logo)) # <input class="form-control-static" id="logo" name="logo" required type="file"> <class 'wtforms.fields.simple.FileField'>
        print(form.logo.data, type(form.logo.data)) # <FileStorage: '2020-07-04_19-54.png' ('image/png')> <class 'werkzeug.datastructures.FileStorage'>
        filename = secure_filename(form.logo.data.filename)
        print(filename,type(filename))  # 2020-07-04_19-54.png <class 'str'>
        print(form.logo.data.filename,type(form.logo.data.filename))# 2020-07-04_19-54.png <class 'str'>
        """
        filename = secure_filename(data['logo'].filename)
        new_filename = change_name(filename)
        """
        print(new_filename) # 20200704214223bac609e7af8b48bc85d0514b8ae17907.png
        """
        if not os.path.exists(app.config['UP']):
            os.makedirs(app.config['UP'])
        form.logo.data.save(app.config['UP'] + new_filename)
        user = User.query.filter_by(name=session['user']).first()  # <User 1> <class 'models.User'>
        article = Article(
            title=data['title'],
            cate_id=data['cate_id'],
            user_id=user.id,
            logo=new_filename,
            content=data['content'],
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(article)
        db.session.commit()
        flash('发布成功！', category='ok')
    return render_template("article_add.html", form=form, title='发布新闻')


@app.route('/article/list/<int:page>/', methods=['GET'])
@user_login_decorator
def article_list(page=None):
    if not page:
        page = 1
    cate = Cate.query.all()
    cate_id_name = [(i.id, i.title) for i in cate]
    cate_id_name.reverse()  # [(1, '科技'), (2, '社会')]
    user = User.query.filter_by(name=session.get('user')).first()
    page_data = Article.query.filter_by(
        user_id=user.id
    ).order_by(
        Article.addtime.desc()
    ).paginate(page=page, per_page=5)
    """
    articles = Article.query.all()
    print(articles, type(articles))  # [<Article 1>, <Article 2>] <class 'list'>
    for article in articles:
        print(article.logo)
    """
    return render_template("article_list.html", title='新闻列表', cate_id_name=cate_id_name, page_data=page_data)


@app.route('/article/edit/<int:id>/', methods=['GET', 'POST'])
@user_login_decorator
def article_edit(id):
    form = ArticleEditForm()
    """
    article = Article.query.filter_by(id=id)
    print(article)  # sql语句
    """
    article = Article.query.filter_by(id=id).first()  # <Article 5>
    if request.method == 'GET':
        form.title.data = article.title
        form.cate_id.data = article.cate_id
        form.content.data = article.content
        form.logo.data = article.logo
    if form.validate_on_submit():
        data = form.data
        """
        print(request.form)
        ImmutableMultiDict([('title', '2020年高考开考 五名全盲考生使用盲文试卷'), ('cate_id', '1'),,,])
        """
        new_filename = secure_filename(change_name(data['logo'].filename))
        try:
            # 标记旧的logo文件
            old_logo_filename = article.logo
            # 更新article中的字段
            article.title = data['title']
            article.cate_id = data['cate_id']
            article.logo = new_filename
            article.content = data['content']
            db.session.add(article)
            db.session.commit()
            # 删除旧的logo文件
            if os.path.exists(app.config['UP'] + old_logo_filename):
                os.remove(app.config['UP'] + old_logo_filename)
            # 保存新的logo文件
            data['logo'].save(app.config['UP'] + new_filename)
            flash('编辑成功！', category='ok')
        except Exception as e:
            print(e.args)
            flash('编辑失败！', category='error')
    return render_template("article_edit.html", form=form,
                           title='<a style="text-decoration:none" href="/article/list/1/">新闻列表</a> >> 编辑新闻',
                           article=article)


@app.route('/article/del/<int:id>/', methods=['GET'])
@user_login_decorator
def article_del(id):
    # print(type(id))  # <class 'int'>
    Article.query.filter_by(id=id).delete()  # 删除的数据行数
    db.session.commit()
    flash('删除成功！', category='ok')
    return redirect('/article/list/1/')


@app.route('/')
@user_login_decorator
def index():
    return redirect('/article/list/1/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error)
