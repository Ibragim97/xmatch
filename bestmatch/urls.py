from django.conf.urls import url
from .  import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rating/', views.rating, name='rating'),
    url(r'^list/', views.listPage, name='listPage'),
    url(r'^top/', views.top, name='top'),
    url(r'^ajax/check_id/', views.check_id, name='check_id'),
]
