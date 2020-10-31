from django.test import TestCase,SimpleTestCase
from trader import forms,templates
from django.test import Client
<<<<<<< HEAD
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


class RegisterPageTest(TestCase):
    def testFormFail1(self):   #สมัครไม่ผ่านเพราะว่าpasswordมีความคล้ายคลึงกับ username
        data={
            'username' : 'testuser',
            'email' : 'test@testmail.com',
            'password1': 'test1234',
            'password2' : 'test1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    
    def testFormFail2(self):   #สมัครไม่ผ่านเพราะว่าpasswordง่ายเกินไป
        data={
            'username' : 'testuser2',
            'email' : 'test2@testmail.com',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def testFormFail3(self):   #สมัครไม่ผ่านเพราะว่า email ไม่ตรงรูปแบบ
        data={
            'username' : 'testuser3',
            'email' : 'test1234',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def testFormFail4(self):   #สมัครผ่าน
        data={
            'username' : 'testuser2',
            'email' : 'test2@testmail.com',
            'password1': 'zazaZA1234',
            'password2' : 'zazaZA1234'
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        
    
class LoginTest(TestCase):
    def setup(self):
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        
    def test_login1(self): ##Login ด้วย username ที่ผิด
        user = authenticate(username='wrong', password='oatty8867')
        self.assertFalse(user is not None and user.is_authenticated)
    def test_correct(self):
        user = authenticate(username='test123', password='oatty8867')
        self.assertTrue((user is not None) and user.is_authenticated)
=======
>>>>>>> 616e366f4f52db073ee26d94c5b427a4234fcd91

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


    
    