from notecard.notecards.models import Semester
from notecard.notecards.models import Section
from notecard.notecards.models import Notecard
from django.contrib import admin

class SemesterAdmin(admin.ModelAdmin):
    model = Semester

class SectionAdmin(admin.ModelAdmin):
    model = Section

class NotecardAdmin(admin.ModelAdmin):
    model = Notecard


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Notecard, NotecardAdmin)