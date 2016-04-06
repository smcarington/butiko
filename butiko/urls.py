from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^list/(?P<pk>\d+)/$', views.list_detail, name='list_detail'),
]
