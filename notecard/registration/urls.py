from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^register/', 'notecard.registration.views.UserRegistration'),
    url(r'^login/$', 'notecard.registration.views.LoginRequest'),
    url(r'^logout/$', 'notecard.registration.views.LogoutRequest'),
)
