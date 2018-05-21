from django.shortcuts import render,redirect,reverse,get_object_or_404

# Create your views here.

#提交评论
from django.views.generic import CreateView

from blog.models import Post
from comments.models import Comment
from comments.forms import CommentModelForm


def post_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    form = CommentModelForm()
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id=pk
            comment.save()
        else:
            context ={
                'post':post,
                'form':form,
                'comment_list': post.comment_set.all()
            }
            return render(request,'blog/detail.html',context)
    return redirect(post)

class CommentCreateView(CreateView):
    model = Comment
    fields = ['name','email','url','content']
    template_name = 'blog/detail.html'
    context_object_name = 'comment_list'

    #重写get_success_url方法
    def get_success_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.kwargs.get('pk')})

    #重写form_valid方法，补全comment需要的post
    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)

    #重写get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs.get('pk'))

        context.update({
            'post': post,
            'comment_list': post.comment_set.all()
        })
        return context
    #当form表单校验不通过时，执行form_invalid
    def form_invalid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return render(self.request,'blog/detail.html',{
            'post': post,
            'comment_list': post.comment_set.all()
        }
                      )










