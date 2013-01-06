from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from notecard.markdown import markdown

class Semester(models.Model):
    semester_name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.semester_name
    
class Section(models.Model):
    section_name = models.CharField(max_length=50)
    semester = models.ForeignKey(Semester)
    
    def __unicode__(self):
        return self.section_name
        
class Notecard(models.Model):
    notecard_name = models.TextField()
    notecard_name_html = models.TextField(editable=False, blank=True)
    notecard_body = models.TextField()
    notecard_html = models.TextField(editable=False, blank=True)
    section = models.ForeignKey(Section)
    known = models.BooleanField()
    
    def save(self, *args, **kwargs):
        self.notecard_html = markdown(self.notecard_body)
        self.notecard_name_html = markdown(self.notecard_name)
        super(Notecard, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.notecard_name

class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        exclude = ('user',)

class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ('semester',)
        
class NotecardForm(ModelForm):
    class Meta:
        model = Notecard
        exclude = ('section', 'known',)
