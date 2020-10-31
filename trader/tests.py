from django.test import TestCase,SimpleTestCase
from trader import forms,templates
from django.test import Client

class RegisterPageTest(TestCase):
    def setup(self):
        self.username1 = 'testuser1'
        self.email1 = 'testuser1@email.com'
        self.password1 = '123456789'
        self.password2 = '123456789'
        self.username2 = 'testuser2'
        self.email2 = 'testuser2@email.com'
        self.password3 = 'gfd5g4er6gs4dk'
        self.password4 = 'gfd5g4er6gs4dk'


class SimpleTests(SimpleTestCase):
    def test_Register_Page_url(self):
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template_name='register')


    
    