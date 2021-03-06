from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^list/(?P<pk>\d+)/$', views.list_detail, name='list_detail'),
    url(r'^list/change_item_count/$', views.change_item_count, name='change_item_count'),
    url(r'^list/delete_item/(?P<objectStr>[a-z]+)/(?P<pk>\d+)/$', views.delete_item, name='delete_item'),
    url(r'^list/add_new_item/(?P<listpk>\d+)/$', views.add_new_item, name='add_new_item'),
    url(r'^list/add_new_list/$', views.add_new_list, name='add_new_list'),
    url(r'^list_search/$', views.list_search, name='list_search'),
    url(r'^suggest_list/$', views.suggest_list, name='suggest_list'),
    url(r'^request_perm/(?P<listpk>\d+)/$', views.request_perm, name='request_perm'),
    url(r'^grant_deny/$', views.grant_deny, name='grant_deny'),
]
