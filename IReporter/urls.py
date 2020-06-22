from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import flag_list,flag_detail
from .views import CreateUserAPIView,LoginApiView,ProfileList,SingleProfile
from django.urls import path,re_path 
from .views import InterventionList, CreateInterventionRecord, InterventionDetail, InterventionListStatus,AllInterventionRecords,

app_name='IReporter'

urlpatterns=[
    url(r'^all-intervention-records/$',AllInterventionRecords.as_view(), name='AllInterventionRecords'),
    url(r'^intervention-records/(?P<title>[A-Za-z]+)/$',InterventionList.as_view(), name='fetch-intervention-records'),
    url(r'^create-intervention-record/$', CreateInterventionRecord.as_view(), name='create-intervention-item'),
    url(r'^intervention-record-detail/(?P<pk>[0-9]+)/$',InterventionDetail.as_view(), name='intervention-detail'),
    url(r'^intervention-records-status/(?P<intervention_status>[A-Za-z]+)/$' ,InterventionListStatus.as_view(), name='filter-by-status'),
    url(r'^api/flags/$',flag_list.as_view()),
    url(r'^api/flags/(?P<pk>[0-9]+)$',flag_detail.as_view())
    url(r'^api/profiles$',ProfileList.as_view()),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view()),
    url(r'^signup/$', CreateUserAPIView.as_view()),
    url(r'^login/$', LoginApiView.as_view()),
]

