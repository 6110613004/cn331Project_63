from django.test import TestCase,SimpleTestCase
from trader import forms,templates
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model


class RegisterFormTest(TestCase):
    def test_form_fail1(self):   #สมัครไม่ผ่านเพราะว่าpasswordมีความคล้ายคลึงกับ username
        data={
            'username' : 'testuser',
            'email' : 'test@testmail.com',
            'password1': 'test1234',
            'password2' : 'test1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    
    def test_form_fail2(self):   #สมัครไม่ผ่านเพราะว่าpasswordง่ายเกินไป
        data={
            'username' : 'testuser2',
            'email' : 'test2@testmail.com',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_form_fail3(self):   #สมัครไม่ผ่านเพราะว่า email ไม่ตรงรูปแบบ
        data={
            'username' : 'testuser3',
            'email' : 'test1234',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_form_success(self):   #สมัครผ่าน
        data={
            'username' : 'testuser4',
            'email' : 'test2@testmail.com',
            'password1': 'zazaZA1234',
            'password2' : 'zazaZA1234'
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
    
        
    
class RegisterTest(TestCase):
    def setup(self):
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        
    def test_login_userfail(self): ##Login ด้วย username ที่ผิด
        self.user = authenticate(username='wrong', password='oatty8867')
        #Should not be able to login
        self.assertFalse(self.user is not None and user.is_authenticated)
    def test_login_passfail(self):
        self.user = authenticate(username='test123',password='123')
        self.assertFalse(self.user is not None and self.user.is_authenticated)
    def test_login_correct(self):
        User = authenticate(username='test123',password='oatty8867')
        self.assertTrue(User is not None and User.is_authenticated)    
# Create your tests here.


