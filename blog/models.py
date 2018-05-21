from django.db import models
# Create your models here.
from django.utils.html import strip_tags
from markdown import Markdown
#定义帖子模型
from django.urls import reverse


#扩展User模型



class Post(models.Model):
    title = models.CharField(max_length=200,verbose_name='标题')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    excerpt = models.CharField(max_length=300,verbose_name='摘要',null=True,blank=True)
    content = models.TextField(verbose_name='内容')
    #作者
    author =models.ForeignKey('users.User',verbose_name='作者')
    #类别
    category =models.ForeignKey('Category',verbose_name='类别')
    #标签云
    tags =models.ManyToManyField('Tag',verbose_name='标签')
    #阅读数
    views = models.PositiveIntegerField(verbose_name='阅读数',default=0)
    class Meta:
        ordering = ['-created_time']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.pk})
    #阅读数增加
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])
    #重写sava,实现自动摘要
    def save(self,*args,**kwargs):
        #判断是否存在摘要
        if not self.excerpt:
            #生成Markdown的实例对象，
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            self.excerpt = strip_tags(md.convert(self.content))[:54]
        super().save(*args,**kwargs)
#类别
class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name='类别')
    def __str__(self):
        return self.name

#标签云
class Tag(models.Model):
    tag_name =models.CharField(max_length=30,verbose_name='标签云')
    def __str__(self):
        return self.tag_name













