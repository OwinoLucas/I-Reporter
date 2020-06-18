from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import intervention_list,intervention_detail,intervention_list_status
urlpatterns=[
    url(r'^api/interventionrecords/$',intervention_list.as_view()),
    url(r'^api/interventionrecords/(?P<pk>[0-9]+)$',intervention_detail.as_view()),
    url(r'api/interventionrecords/resolved/$' ,intervention_list_status.as_view())
]