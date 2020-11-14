from django.test import TestCase,SimpleTestCase
from trader import forms,signals
from .models import Product,Profile
from django.test import Client
from django.urls import reverse
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import MagicMock
from django.contrib.admin.sites import AdminSite




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
    
    def test_form_fail_4(self):
        data={}
        form=UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_form_success(self):   #สมัครผ่าน Happy path
        data={
            'username' : 'testuser4',
            'email' : 'test2@testmail.com',
            'password1': 'zazaZA1234',
            'password2' : 'zazaZA1234'
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
    
    
class RegisterTest(TestCase):     
    def test_login_userfail(self): ##Login ด้วย username ที่ผิด
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        self.user = authenticate(username='wrong', password='oatty8867')
        #Should not be able to login
        self.assertFalse(self.user is not None and user.is_authenticated)
    def test_login_passfail(self):
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        self.user = authenticate(username='test123',password='123')
        self.assertFalse(self.user is not None and self.user.is_authenticated)
    def test_login_correct(self):
        User = get_user_model()
        self.user=User.objects.create_user('test123','test@testmail.com','oatty8867')
        self.user.save()
        User = authenticate(username='test123', email='test@testmail.com', password='oatty8867')
        self.assertTrue(User is not None and User.is_authenticated)    

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details_aboutpage(self): ##Testหน้าaboutpage
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_details_myshop(self):  ##Testหน้าmyshop
        # Issue a GET request.
        response = self.client.get('/myshop')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_details_shop(self): ##Testหน้าshop
        # Issue a GET request.
        response = self.client.get('/shop')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_details_addproductpage(self): ##Testหน้าaddproduct
        # Issue a GET request.
        response = self.client.get('/addproductpage')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    def test_details_productpage(self):  ##Testproductpage
        # Issue a GET request.
        response = self.client.get('/productpage/<str:x_ownerName>')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

class TestModelProfile(TestCase):  #test profile objects amount Happy path
    def test_object_count(self):
        user1 = User.objects.create_user('test123','test@mail.com','oatty8867')
        self.assertEqual(Profile.objects.count(),1) #Profile object should be 1

class TestModelProduct(TestCase):  
    def test_object_productcount(self):  #test product objects
        User.objects.create_user('Oatty','test@mail.com','oatty8867')
        user1 = User.objects.get(username='Oatty')
        product1 = Product(pName='Book',ownerName='Harry')
        self.assertEqual(product1.pName,'Book')
        self.assertEqual(product1.ownerName,'Harry')
        ############################################################################################################
class TestDelete(TestCase):

    def test_Delete(self):
        Product.objects.create(pName='Book',ownerName='Harry')
        temp = Product.objects.get(pName='Book')
        temp.delete()
        if Product.objects.count() == 1:
            status = False
        elif Product.objects.count() == 0:
            status = True
        response = self.client.get('/myshop')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(status, True)
        
class TestSearch(TestCase):

    def test_Search(self):
        Product.objects.create(pName='Book',ownerName='Harry')
        temp = Product.objects.get(pName='Book')
        if temp.pName == 'Book':
            status = True
        else:
            status = False
        response = self.client.get('/searchbar/?search=Book')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(status, True)


##Test Signal here
class TestSignals(TestCase):
    def test_create_profile_signal_triggered(self):
        handler = MagicMock()
        signals.create_profile.send(handler, sender='test')
        
        form = UserCreationForm()
        form.cleaned_data={'username':'oatty111','email':'oatty@mail.com','password1':'test123',
        'password2':'test123','first_name':'Michael','last_name':'Jordan'}
        form.save()
        signals.create_profile.send(sender='test',form_date=form)

        handler.assert_called_once_with(signal=signals.create_profile, form_data=form, sender='test')






