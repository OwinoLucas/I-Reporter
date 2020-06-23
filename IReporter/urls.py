from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import FlagDetail,FlagStatus,AllFlagRecords,CreateFlag,FlagList
from .views import CreateUserAPIView,LoginApiView,ProfileList,SingleProfile
from django.urls import path,re_path 
from .views import InterventionList, CreateInterventionRecord, InterventionDetail, InterventionListStatus,AllInterventionRecords,

app_name='IReporter'

urlpatterns=[
    url(r'^api/profiles$',ProfileList.as_view(),name="profilelist"),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view(),name="singleprofile"),
    url(r'^all-intervention-records/$',AllInterventionRecords.as_view(), name='AllInterventionRecords'),
    url(r'^intervention-records/(?P<title>[A-Za-z]+)/$',InterventionList.as_view(), name='fetch-intervention-records'),
    url(r'^create-intervention-record/$', CreateInterventionRecord.as_view(), name='create-intervention-item'),
    url(r'^intervention-record-detail/(?P<pk>[0-9]+)/$',InterventionDetail.as_view(), name='intervention-detail'),
    url(r'^intervention-records-status/(?P<intervention_status>[A-Za-z]+)/$' ,InterventionListStatus.as_view(), name='filter-by-status'),
    url(r'^api/profiles$',ProfileList.as_view()),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view()),
    url(r'^api/flags/$',AllFlagRecords.as_view(),name='allflags'),
    url(r'^api/flags/(?P<pk>[0-9]+)$',FlagDetail.as_view()),
    url(r'^api/flags/create/$',CreateFlag.as_view()),
    url(r'^api/flags/status(?P<flag_status>[A-Za-z]+)/$' ,FlagStatus.as_view(), name='filter-by-status'),
    url(r'^Flags/(?P<title>[A-Za-z]+)/$',FlagList.as_view(), name='flag list records fetch'),
    url(r'^signup/$', CreateUserAPIView.as_view()),
    url(r'^login/$', LoginApiView.as_view()),
]

