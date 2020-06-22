from django.conf.urls import url
from . import views
from .views import CreateUserAPIView,LoginApiView,intervention_list,intervention_detail,intervention_list_status,ProfileList,SingleProfile
from django.urls import path,re_path 

app_name='IReporter'
urlpatterns=[
    url(r'^api/profiles$',ProfileList.as_view(),name="profilelist"),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view(),name="singleprofile"),
    url(r'^signup/$', CreateUserAPIView.as_view()),
    url(r'^login/$', LoginApiView.as_view()),
    url(r'^api/interventionrecords/$',intervention_list.as_view()),
    url(r'^api/interventionrecords/(?P<pk>[0-9]+)$',intervention_detail.as_view()),
    url(r'api/interventionrecords/resolved/$' ,intervention_list_status.as_view()), 
]