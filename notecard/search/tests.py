from django.test import TestCase
from notecard.notecards.models import *
from django.contrib.auth.models import User
from django.test import TestCase, Client


class SearchTest(TestCase):
    def setUp(self):
        self.User = User.objects.create_user('Dan', 'DHoerst1@gmail.com', 'danpass')
        self.Semester = Semester.objects.create(semester_name="CS103", user=self.User)        
        self.Section = Section.objects.create(section_name="Section 1", semester=self.Semester)
        self.Notecard = Notecard.objects.create(notecard_name="Test Notecard", notecard_body="This is a test we will find test", notecard_html="", section=self.Section)
        self.Notecard = Notecard.objects.create(notecard_name="No Notecard", notecard_body="This will not show up in search", notecard_html="", section=self.Section)
        
