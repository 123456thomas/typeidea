# -*- coding: utf-8 -*-
# @Time    : 2020/2/2 11:34
# @Author  : ManStein
# @Email   : 17625809083@163.com
# @File    : develop.py
# @Software: PyCharm
from .base import *  # NOQA

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}