from django.conf.urls import url
from . import views
from django.urls import path,re_path 
urlpatterns=[
    path('api/interventionrecords',views.intervention_list),
    re_path(r'^api/interventionrecords/(?P<pk>[0-9]+)$',views.intervention_detail),
    path(r'api/interventionrecords/resolved' ,views.intervention_list_resolved)
]