from django.test import TestCase, Client
import django.contrib.auth.models

class UserTest(TestCase):
    def test_registration(self):
        c = Client()
        response = c.post('/auth/register/', {'username': 'test', 'password1': 'test', 'password2': 'test',})
        self.assertEqual(response.status_code, 302)
        user = django.contrib.auth.models.User.objects.get(username='test')
        self.assertEqual(user.username, 'test')
        
    def test_login(self):
        self.User = django.contrib.auth.models.User.objects.create_user('Dan', 'DHoerst1@gmail.com', 'danpass')
        c = Client()
        response = c.post('/auth/login/', {'username': 'Dan', 'password': 'danpass',})
        user = django.contrib.auth.models.User.objects.get(username='Dan')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], user.pk)