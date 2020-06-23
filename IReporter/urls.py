from django.conf.urls import url
from .views import intervention_list,intervention_detail,intervention_list_status,CreateUserAPIView
# from django.urls import path 

app_name='IReporter'
urlpatterns=[
    url(r'^signup/$', CreateUserAPIView.as_view()),
    # url(r'^login/$', LoginApiView.as_view()),
    url(r'^api/interventionrecords/$',intervention_list.as_view()),
    url(r'^api/interventionrecords/(?P<pk>[0-9]+)$',intervention_detail.as_view()),
    url(r'api/interventionrecords/resolved/$' ,intervention_list_status.as_view()), 
]