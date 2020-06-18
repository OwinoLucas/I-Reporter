from django.conf.urls import url
from .views import CreateUserAPIView
from . import views

urlpatterns=[
    url(r'^signup/$', CreateUserAPIView.as_view()),
]