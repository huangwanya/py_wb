from django.conf.urls import url,include
from . import views


app_name = 'apps1'
urlpatterns = [
    url(r'^$',views.fenxi,name='index'),
    url(r'user/', views.myuser, name='myuser'),
    url(r'myuser_update_s/', views.myuser_update, name='myuser_update_s'),
    url(r'fenxi/', views.fenxi, name='fenxi'),
    url(r'tubiao/', views.tubiao, name='tubiao'),
    url(r'pinglun/', views.pinglun, name='pinglun'),
]