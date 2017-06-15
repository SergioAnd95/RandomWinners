from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NameCreateView.as_view(), name='create_name'),
    url(r'^get_winners/$', views.get_winners, name='get_winners'),
    url(r'^refresh_winners/$', views.refresh_winners, name='refresh_winners'),
    url(r'^remove_candiate/(?P<pk>[0-9]+)/$', views.remove_candidate, name='remove_candidate')
]