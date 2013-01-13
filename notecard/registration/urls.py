from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^register/', 'registration.views.UserRegistration'),
    url(r'^login/$', 'registration.views.LoginRequest'),
    url(r'^logout/$', 'registration.views.LogoutRequest'),
    url(r'^mailreset/$', 'registration.views.PasswordReset')
)
