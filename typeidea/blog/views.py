from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Post, Tag, Category
from config.models import SideBar
# Create your views here.


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content.update({'sidebars': SideBar.get_all()})
        content.update(Category.get_navs())
        return content


class IndexView(CommonViewMixin, ListView):
    """展示蚊帐列表，每页10个"""
    queryset = Post.latest_posts()
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        content.update({'category': category})
        content.update(Category.get_navs())
        return content

    def get_queryset(self):
        """重写queryset, 根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        print(tag_id ,'====>')
        tag = get_object_or_404(Tag, pk=tag_id)
        content.update({'tag': tag})
        return content

    def get_queryset(self):
        """重写queryset, 根据分类过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    # model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


def list_post(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category= Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        print('get_context_data: ==>',context)
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        print('get_queryset: ==>', keyword)
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs.get('user_id')
        return queryset.filter(owner_id=user_id)