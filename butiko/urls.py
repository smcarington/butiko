from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^list/(?P<pk>\d+)/$', views.list_detail, name='list_detail'),
    url(r'^list/change_item_count/$', views.change_item_count, name='change_item_count'),
    url(r'^list/delete_item/(?P<pk>\d+)/$', views.delete_item, name='delete_item'),
    url(r'^list/add_new_item/(?P<listpk>\d+)/$', views.add_new_item, name='add_new_item'),
    url(r'^list/add_new_list/$', views.add_new_list, name='add_new_list'),
]
