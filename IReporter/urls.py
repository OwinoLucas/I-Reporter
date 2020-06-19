from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import flag_list,flag_detail
urlpatterns=[
    url(r'^api/flags/$',flag_list.as_view()),
    url(r'^api/flags/(?P<pk>[0-9]+)$',flag_detail.as_view())
]