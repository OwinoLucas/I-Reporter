from django.conf.urls import url
from . import views
from IReporter.views import ProfileList,SingleProfile

urlpatterns=[
    url(r'^api/profiles$',ProfileList.as_view()),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view()),
]