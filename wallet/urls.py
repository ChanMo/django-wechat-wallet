from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^log_list/$', views.LogListView.as_view(), name='log_list'),
)
