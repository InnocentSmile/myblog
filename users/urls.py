from django.conf.urls import url
from .views import register,EditUserView

app_name ='users'

urlpatterns = [
    url('^register/$',register,name='register'),

    url('^edit_user/(?P<pk>\d+)/$',EditUserView.as_view(),name='edit_user')

]