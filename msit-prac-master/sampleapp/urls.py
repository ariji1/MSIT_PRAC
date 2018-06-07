from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'sampleapp'

# Basics
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^about/$', views.about_view, name='about'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]

# Create an account
urlpatterns += [
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^signup/$', views.signup_view, name='signup'),
]

# Existing account operations
urlpatterns += [
    url(r'^change/$', views.change_pwd, name='change_pwd'),
    url(r'^home/$', views.home_view, name='home'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^error/$', views.error_view, name='error'),
]

# Authentication operations
urlpatterns += [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
]

# Chat operations
urlpatterns += [
    url(r'^chat/(?P<u>[a-zA-Z0-9_]+)/$', views.chat_with, name='chat'),
]

# LOGIN_URL = 'signin'
# LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'home'
