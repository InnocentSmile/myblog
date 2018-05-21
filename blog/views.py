from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from markdown.extensions.toc import TocExtension

from blog.utils import custom_paginator
from comments.forms import CommentModelForm
from .models import Post,Tag
import markdown
from django.utils.text import slugify
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})
def index(request):
    post_list = Post.objects.all()
    #对post_list进行分页
    paginator = Paginator(post_list,3)
    page = request.GET.get('page',None)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts =paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #把页对象返回
    return render(request,'blog/index.html',{'posts':posts})

class PostListview(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        start,end = custom_paginator(current_page=page_obj.number,num_page=paginator.num_pages,max_page=4)
        context.update({
            'page_range':range(start,end+1)
        })
        return context



def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.content = markdown.markdown(post.content,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form =CommentModelForm()
    #评论列表
    comment_list = post.comment_set.all()
    #调用阅读数增加的方法
    post.increase_views()
    context = {
        'post': post,
        'form': form,
        'comment_list':comment_list
    }
    return render(request,'blog/detail.html',context)

#将detail函数转换成通用类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    # 重写get方法，以调用increase_views方法
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    # 重写get_object方法，以调用markdown方法渲染post的content
    def get_object(self, queryset=None):
        #获取对象
        self.object =super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        self.object.content = md.convert(self.object.content)
        self.object.toc = md.toc
        #返回object
        return self.object
    #重写get_context_data方法，放入自己的上下文
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = self.object.comment_set.all()
        # 对post_list进行分页
        paginator = Paginator(comment_list, 3)
        page = self.request.GET.get('page', None)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        start, end = custom_paginator(current_page=comments.number, num_page=paginator.num_pages, max_page=4)
        context.update({
            'form': CommentModelForm(),
            'comments': comments,
            'page_range':range(start,end+1),
        })
        return context


#优化PostDetailView
class PostDetailViewPrime(SingleObjectMixin,ListView):
    template_name = 'blog/detail.html'
    paginate_by = 3
    # 重写get方法
    def get(self, request, *args, **kwargs):
        self.object =self.get_object(queryset=Post.objects.all())
        self.object.increase_views()
        return super().get(request, *args, **kwargs)
    #重写get_object
    def get_object(self, queryset=Post.objects.all()):
        post = super().get_object(queryset=Post.objects.all())
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        # 返回object
        return post
    #重写get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        start, end = custom_paginator(current_page=page_obj.number, num_page=paginator.num_pages, max_page=4)
        context.update({
            'form':CommentModelForm(),
            'page_range': range(start, end + 1)
        })
        return context
    def get_queryset(self):
        return self.object.comment_set.all()


#归档
class ArchivesListView(PostListview):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs['year'],created_time__month=self.kwargs['month'])
#分类
class CategoriesListView(PostListview):
    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk']).order_by('-created_time')

#标签
class TagsListView(PostListview):
    def get_queryset(self):
        # tag =get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        # return super().get_queryset().filter(tags=tag).order_by('-created_time')

        # return super().get_queryset().filter(tags__id=self.kwargs['pk']).order_by('-created_time')
        return super().get_queryset().filter(tags=self.kwargs['pk']).order_by('-created_time')

# def search(request):
#     q = request.GET.get('q',None)
#     #判断能不能获取到关键词
#     if q:
#         post_list=Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
#         return render(request,'blog/index.html',{'object_list':post_list})
#     else:
#         msg = '请输入搜索的内容'
#         return render(request,'blog/index.html',{'msg':msg})








