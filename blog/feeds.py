from django.contrib.syndication.views import Feed

from .models import Post

#定义rss订阅的feed
class AllPostFeed(Feed):
    title = '千峰博客'
    link = '/blog/index/'
    description ='千峰博客'
    def items(self):
        return Post.objects.all()
    def item_title(self, item):
        return '[%s]%s' % (item.category,item.title)
    def item_description(self, item):
        return item.content







