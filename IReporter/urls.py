from django.conf.urls import url
from .views import LoginApiView

app_name='IReporter'
urlpatterns=[
    url(r'^login/$', LoginApiView.as_view()),
    
]