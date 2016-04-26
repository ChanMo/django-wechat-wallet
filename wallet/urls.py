from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^recharge/$', views.Recharge.as_view(), name='recharge'),
    url(r'^pay/$', views.Pay.as_view(), name='pay'),
    url(r'^log_list/$', views.LogList.as_view(), name='log_list'),
    url(r'^recharge_notify/$', views.PayNotify.as_view(), name='recharge_notify'),
)
