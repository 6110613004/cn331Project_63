from django.test import TestCase,SimpleTestCase
from trader import forms
from .models import Product,Profile
from django.test import Client
from django.urls import reverse
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile



class RegisterFormTest(TestCase):
    def test_form_fail_1(self):   #สมัครไม่ผ่านเพราะว่าpasswordมีความคล้ายคลึงกับ username Bad path
        data={
            'username' : 'testuser',
            'email' : 'test@testmail.com',
            'password1': 'test1234',
            'password2' : 'test1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    
    def test_form_fail_2(self):   #สมัครไม่ผ่านเพราะว่าpasswordง่ายเกินไป Bad path
        data={
            'username' : 'testuser2',
            'email' : 'test2@testmail.com',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_form_fail_3(self):   #สมัครไม่ผ่านเพราะว่า email ไม่ตรงรูปแบบ Bad path
        data={
            'username' : 'testuser3',
            'email' : 'test1234',
            'password1': '1234',
            'password2' : '1234'
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_form_success(self):   #สมัครผ่าน Good path
        data={
            'username' : 'testuser4',
            'email' : 'test2@testmail.com',
            'password1': 'zazaZA1234',
            'password2' : 'zazaZA1234'
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
    
        
    
class RegisterTest(TestCase):     
    def test_login_userfail(self): ##Login ด้วย username ที่ผิด Bad path
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        self.user = authenticate(username='wrong', password='oatty8867')
        #Should not be able to login
        self.assertFalse(self.user is not None and user.is_authenticated)
    def test_login_passfail(self): ##Login ไม่ผ่านเพราะ password ผิด Bad path
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        self.user = authenticate(username='test123',password='123')
        #Should not be able to login
        self.assertFalse(self.user is not None and self.user.is_authenticated)
    def test_login_correct(self): ##Login ผ่าน Happy path
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        User = authenticate(username='test123', email='test@testmail.com', password='oatty8867')
        #Should be able to login
        self.assertTrue(User is not None and User.is_authenticated)

class TestModelProfile(TestCase):  #test profile objects amount Happy path
    def test_object_count(self):
        user1 = User.objects.create_user('test123','test@mail.com','oatty8867')
        self.assertEqual(Profile.objects.count(),1) #Profile object should be 1




