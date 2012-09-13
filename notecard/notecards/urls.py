from django.conf.urls import *
import notecard.notecards.views

urlpatterns = patterns('',
    url(r'^new/(?P<semester_id>[\w|\W]+)/new_section/$', notecard.notecards.views.new_section, name="new_section"),
    url(r'^new/new_semester/$', notecard.notecards.views.new_semester, name="new_semester"),
    url(r'^new/(?P<section_id>[\w|\W]+)/new_notecard/$', notecard.notecards.views.new_notecard, name="new_notecard"),
)
urlpatterns += patterns('',
    url(r'^semester/(?P<semester_id>[\w|\W]+)/edit/$', notecard.notecards.views.edit_semester, name="edit_semester"),
    url(r'^section/(?P<section_id>[\w|\W]+)/edit/$', notecard.notecards.views.edit_section, name="edit_section"),
    url(r'^notecard/(?P<notecard_id>[\w|\W]+)/edit/$', notecard.notecards.views.edit_notecard, name="edit_notecard"),
)
urlpatterns += patterns('',
    url(r'^(?P<section_id>[\w|\W]+)/unknown/$', notecard.notecards.views.unknown_list, name="unknown_list"),
    url(r'^(?P<section_id>[\w|\W]+)/known/', notecard.notecards.views.known_list, name="known_list"),
    url(r'^semester/(?P<semester_id>[\w|\W]+)/', notecard.notecards.views.section_list, name="section_list"),
    url(r'^section/(?P<section_id>[\w|\W]+)/', notecard.notecards.views.notecard_list, name="notecard_list"),
    url(r'^notecard/(?P<notecard_id>[\w|\W]+)/', notecard.notecards.views.notecard_detail, name="notecard_detail"),
    url(r'^movetoknown/(?P<notecard_id>[\w|\W]+)/', notecard.notecards.views.toggle_known, name="toggle_known"),
    url(r'^$', notecard.notecards.views.semester_list, name="semester_list"),
)
