# coding:utf8
# @Time : 2020/7/2 上午2:22
# @Author : Erics
# @File : manage.py
# @Software: PyCharm
from views import app

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)