from django.conf.urls import url
from . import views

# r'^$' does match an empty string. ^ with the start and $ with the end
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # ex: /polls/recent/2
    url(r'^recent/(?P<n_polls>[0-9]+)/$', views.recent, name='recent'),
]