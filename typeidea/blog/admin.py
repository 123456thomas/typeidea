from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from .models import Category, Tag, Post
from typeidea.custom_site import custom_site


# Register your models here.
# 在admin页面查看日志
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')


class PostInline(admin.TabularInline):
    """
    实现分类页面编辑文章
    """
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj): # 统计分类下的文章数目
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'status', 'owner', 'created_time', 'operator']
    list_display_links = []
    list_filter = (CategoryOwnerFilter,)
    search_fields = ('title', 'category__name',)
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    exclude = ('owner',)
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('category', 'title'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    filter_vertical = ('tag',)

    def operator(self, obj):
        return  format_html(
            '< href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    class Media:
        css = {
            'all': ('https://github.com/bootcdn/BootCDN/tree/1.0.1/ajax/libs/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://github.com/bootcdn/BootCDN/tree/1.0.1/ajax/libs/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)