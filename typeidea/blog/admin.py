from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post
from typeidea.custom_site import custom_site


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):  # 获取当前作者（外键），并保存
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj): # 统计分类下的文章数目
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def get_queryset(self, request):  # 只显示作者的分类
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'post_count')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):  # 获取当前作者（外键），并保存
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj): # 统计分类下的文章数目
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def get_queryset(self, request):  # 只显示作者的标签
        qs = super(TagAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

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
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'operator']
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

    def operator(self, obj):
        return  format_html(
            '< href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):  # 只显示作者的文章
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)