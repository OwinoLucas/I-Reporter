from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import intervention_list
urlpatterns=[
    path(r'api/interventionrecords',intervention_list.as_view()),
    re_path(r'^api/interventionrecords/(?P<pk>[0-9]+)$',views.intervention_detail),
    path(r'api/interventionrecords/resolved' ,views.intervention_list_resolved)
]