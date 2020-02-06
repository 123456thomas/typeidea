# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 15:41
# @Author  : ManStein
# @Email   : 17625809083@163.com
# @File    : adminforms.py
# @Software: PyCharm

from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)