from django.conf.urls import url
from . import views

# app_name = 'posts'
urlpatterns = [
	url(r'^$', views.post_list, name='list'),
	url(r'^create$', views.post_create, name='create'),
	url(r'^(?P<slug>[a-z0-9-]+)/$', views.post_detail, name='detail'),
	url(r'^(?P<slug>[a-z0-9-]+)/edit$', views.post_update, name='update'),
	url(r'^(?P<slug>[a-z0-9-]+)/delete$', views.post_delete, name='delete'),
]