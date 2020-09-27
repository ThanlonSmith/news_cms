# coding:utf8
# @Time : 2020/7/2 上午1:27
# @Author : Erics
# @File : models.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy  # pip install flask_sqlalchemy

from create_app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost:3306/article_cms?charset=UTF8MB4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"  # 指定表名，也可以不加这行代码SQLAlchemy会自动生成表名
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(20), nullable=False, unique=True)  # 账号
    pwd = db.Column(db.String(100), nullable=False)  # 密码
    addtime = db.Column(db.DateTime, nullable=False)  # 注册时间


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), nullable=False)  # 标题
    logo = db.Column(db.String(100), nullable=False)  # 封面
    content = db.Column(db.Text, nullable=False)  # 内容
    addtime = db.Column(db.DateTime, nullable=False)  # 发布时间
    user_id = db.Column(db.Integer, nullable=False)  # 作者id
    cate_id = db.Column(db.Integer, nullable=False)  # 分类id


class Cate(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(10), unique=True)  # 分类名称


if __name__ == '__main__':
    # 如果表已存在就不会再创建
    db.create_all()  # 创建所有的表
