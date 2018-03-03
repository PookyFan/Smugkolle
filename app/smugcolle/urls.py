# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views as auth_views
import smugcolle.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.log_in, name='login'),
	url(r'^logout/$', views.log_out, name='logout'),
	url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^smug/random', views.get_random_smug, name='get_random'),
	url(r'^smug/manage/$', views.manage_smugs, name='manage_images'),
	url(r'^smug/add/$', views.add_smug),
	url(r'^smug/add_many/$', views.add_many_smugs, name='add_many'),
	url(r'^smug/delete/(?P<img_id>[\d]+)/$', views.delete_smug, name='delete'),
	url(r'^get_token/', auth_views.obtain_auth_token),
]
