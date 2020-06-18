from django.conf.urls import url
from .views import CreateUserAPIView
from . import views
from .views import LoginApiView


urlpatterns=[
    url(r'^signup/$', CreateUserAPIView.as_view()),
    url(r'^login/$', LoginApiView.as_view()),
    
]