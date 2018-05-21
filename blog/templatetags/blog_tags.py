from django import template
from django.db.models import Count

from blog.models import Post, Category, Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


#归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

#分类
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#标签云
@register.simple_tag
def get_Tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # return Tag.objects.all()

