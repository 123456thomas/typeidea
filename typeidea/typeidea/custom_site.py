# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 23:00
# @Author  : ManStein
# @Email   : 17625809083@163.com
# @File    : custom_site.py
# @Software: PyCharm
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typeides'
    site_title = 'Typeidea管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')