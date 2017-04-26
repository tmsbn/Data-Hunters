from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^load$', views.load_data, name='load_data'),
    url(r'^delete$', views.delete_data, name='delete_data'),
    url(r'^show$', views.show_all_data, name='show_all_data'),
]