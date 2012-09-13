from notecard.notecards.models import *
from django.contrib.auth.models import User
from django.test import TestCase

class SemesterTest(TestCase):
    def setUp(self):
        self.User = User.objects.create_user('Dan', 'DHoerst1@gmail.com', 'danpass')
        self.CS103 = Semester.objects.create(semester_name="CS103", user=self.User)
        self.CS212 = Semester.objects.create(semester_name="CS212", user=self.User)
        self.StringSemester = Semester.objects.create(semester_name="TestSemester", user=self.User)
        self.SpaceSemester = Semester.objects.create(semester_name="Test Semester", user=self.User)
        self.NumberSemester = Semester.objects.create(semester_name="123456", user=self.User)
        self.SymbolSemester = Semester.objects.create(semester_name="!@#$%^&*()-+=", user=self.User)
    
    def test_semester_name(self):
        self.assertEqual(self.CS103.semester_name, "CS103")
        self.assertEqual(self.CS212.semester_name, "CS212")
        self.assertEqual(self.StringSemester.semester_name, "TestSemester")
        self.assertEqual(self.SpaceSemester.semester_name, "Test Semester")
        self.assertEqual(self.NumberSemester.semester_name, "123456")
        self.assertEqual(self.SymbolSemester.semester_name, "!@#$%^&*()-+=")
        
    def test_user(self):
        self.assertEqual(self.CS103.user, self.User)
        self.assertEqual(self.CS212.user, self.User)
        self.assertEqual(self.StringSemester.user, self.User)
        self.assertEqual(self.SpaceSemester.user, self.User)
        self.assertEqual(self.NumberSemester.user, self.User)
        self.assertEqual(self.SymbolSemester.user, self.User)

class SectionTest(TestCase):
    def setUp(self):
        self.User = User.objects.create_user('Dan', 'DHoerst1@gmail.com', 'danpass')
        self.Semester = Semester.objects.create(semester_name="CS103", user=self.User)
        self.NumberSection = Section.objects.create(section_name="123456", semester=self.Semester)
        self.StringSection = Section.objects.create(section_name="TestSemester", semester=self.Semester)
        self.SpaceSection = Section.objects.create(section_name="Test Semester", semester=self.Semester)
        self.SymbolSection = Section.objects.create(section_name="!@#$%^&*()-+=", semester=self.Semester)
        
    def test_section_name(self):
        self.assertEqual(self.NumberSection.section_name, "123456")
        self.assertEqual(self.StringSection.section_name, "TestSemester")
        self.assertEqual(self.SpaceSection.section_name, "Test Semester")
        self.assertEqual(self.SymbolSection.section_name, "!@#$%^&*()-+=")
        
    def test_semester(self):
        self.assertEqual(self.NumberSection.semester, self.Semester)
        self.assertEqual(self.StringSection.semester, self.Semester)
        self.assertEqual(self.SpaceSection.semester, self.Semester)
        self.assertEqual(self.SymbolSection.semester, self.Semester)
        
class NotecardTest(TestCase):
    def setUp(self):
        self.User = User.objects.create_user('Dan', 'DHoerst1@gmail.com', 'danpass')
        self.Semester = Semester.objects.create(semester_name="CS103", user=self.User)        
        self.Section = Section.objects.create(section_name="Section 1", semester=self.Semester)
        self.Notecard = Notecard.objects.create(notecard_name="Test Notecard", notecard_body="""Here is an answer hey whats up. 

Here is an answer hey whats up. Here is an answer hey whats up. 

Here is an answer hey whats up.""", notecard_html="", section=self.Section)
        
    def test_notecard_name(self):
        self.assertEqual(self.Notecard.notecard_name, "Test Notecard")
    
    def test_notecard_body(self):
        self.assertEqual(self.Notecard.notecard_body, """Here is an answer hey whats up. 

Here is an answer hey whats up. Here is an answer hey whats up. 

Here is an answer hey whats up.""")
    
    def test_notecard_html(self):
        self.assertEqual(self.Notecard.notecard_html, """<p>Here is an answer hey whats up. </p>
<p>Here is an answer hey whats up. Here is an answer hey whats up. </p>
<p>Here is an answer hey whats up.</p>""")
        
    def test_section(self):
        self.assertEqual(self.Notecard.section, self.Section)
    
    def test_known(self):
        self.assertEqual(self.Notecard.known, 0)