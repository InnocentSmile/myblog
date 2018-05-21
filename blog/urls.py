from django.conf.urls import url
from blog.views import (
    PostListview,
    # post_detail,
    ArchivesListView,
    CategoriesListView,
    PostDetailView,
    TagsListView,
    # search,
    index,
    PostDetailViewPrime,

)

app_name = 'blog'

urlpatterns =[
    url(r'^index/$',PostListview.as_view(),name='index'),
    # url(r'^index/$',index,name='index'),
    # url(r'^post_detail/(?P<pk>\d+)/$',post_detail,name='post_detail'),
    url(r'^post_detail/(?P<pk>\d+)/$',PostDetailViewPrime.as_view(),name='post_detail'),

    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$',ArchivesListView.as_view(),name='archives'),

    url(r'^categories/(?P<pk>\d+)/$',CategoriesListView.as_view(),name='categories'),
    url(r'^tags/(?P<pk>\d+)/$',TagsListView.as_view(),name='tags'),

    # url(r'^search/$',search,name='search')

]



