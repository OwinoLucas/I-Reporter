from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import InterventionList, CreateIntervention, InterventionDetail, InterventionListStatus


urlpatterns=[
    url(r'^intervention-records/(?P<title>[A-Za-z]+)/$',InterventionList.as_view(), name='fetch-intervention-records'),
    url(r'^create-intervention-record/$', CreateIntervention.as_view(), name='create-intervention-item'),
    url(r'^intervention-record-detail/(?P<pk>[0-9]+)/$',InterventionDetail.as_view(), name='intervention-detail'),
    url(r'^intervention-records-status/(?P<intervention_status>[A-Za-z]+)/$' ,InterventionListStatus.as_view(), name='filter-by-status')
]