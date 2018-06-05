from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SubjectsView.as_view(), name='subjects'),
    url(r'^table/download/(?P<hashcode>.+)/$', views.DownloadView.as_view(), name='download'),
    url(r'^table/(?P<hashcode>.+)$', views.TableView.as_view(), name='table'),
    url(r'^ajax/get_subjects', views.get_subjects, name="index"),
    url(r'^refresh_data', views.refresh),
]