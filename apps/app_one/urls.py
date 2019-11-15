from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.check),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books1),
    url(r'^books/add$', views.add),
    url(r'^books/add/process$', views.addprocess),
    url(r'^books/(?P<num>\d+)$', views.showbook),
    url(r'^books/(?P<num>\d+)/addreview$', views.addareview),
    
]
