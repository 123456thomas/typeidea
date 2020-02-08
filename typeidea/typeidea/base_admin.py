# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 23:19
# @Author  : ManStein
# @Email   : 17625809083@163.com
# @File    : base_admin.py
# @Software: PyCharm

from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、右链这些model的owner;
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin,self).save_model(request, obj, form, change)