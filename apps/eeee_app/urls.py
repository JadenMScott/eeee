from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^register$',views.register),
    url(r'^dashboard/(?P<id>\d+)$',views.dashboard),
    url(r'^trip/(?P<id>\d+)$',views.trip),
    url(r'^add_trip$',views.add_trip),
    url(r'^edit_trip/(?P<id>\d+)$',views.edit_trip),
    url(r'^join/(?P<id>\d+)$',views.join),
    url(r'^cancel/(?P<id>\d+)$',views.cancel),
    url(r'^remove/(?P<id>\d+)$',views.remove),

    url(r'^logout$',views.logout),
]