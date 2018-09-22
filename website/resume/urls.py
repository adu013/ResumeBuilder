from django.conf.urls import url
from . import views

app_name = 'resume'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.change_password, name='change_password'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]