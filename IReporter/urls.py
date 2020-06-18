from django.conf.urls import url
from . import views
from IReporter.views import ProfileList 

urlpatterns=[
    url(r'^api/profiles$',ProfileList.as_view()),
]