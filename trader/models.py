from django.db import models
from PIL import Image
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    FACULTY_TU = (
        ('E', 'Faculty of Engineering'),
        ('L', 'Faculty of Law'),
        ('AE', 'Faculty of Architecture'),
        ('DY','Faculty of Dentisty'),
        ('LA','Faculty of Liberal Art'),
        ('PS','Faculty of Political Science'),
        ('M','Faculty of Medicine'),
        ('EM','Faculty of Economics')
    )  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default2.png',upload_to='profile_pics') #Field for profile pic.
    faculty = models.CharField(choices=FACULTY_TU, max_length=2,blank = True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):  #reduced picture sized in database
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Product(models.Model):
    CATEGORY_CHOICES = (
    ('B', 'Books'),
    ('A', 'Accessories'),
    ('OT', 'Other'),
    ('E','Equipment')
)
    pName = models.CharField(max_length = 30)
    owner = models.ManyToManyField(User,blank = True)
    ownerName = models.CharField(max_length = 30,blank = True)
    category = models.CharField( max_length=30,blank = True)
    p_image = models.ImageField(upload_to='product_pics',default = 'dafault1.jpg')
    p_detail = models.CharField(max_length = 200,blank = True)
    p_price = models.CharField(max_length = 6,default = 0)
    pStatus = models.BooleanField(default = True)
   
    
    def save(self,*args,**kwargs):  #reduced picture sized in database
        super(Product, self).save(*args, **kwargs)

        img = Image.open(self.p_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.p_image.path)

    #pDetail = models.TextField(null = True , blank = True)
    #pSell = models.ManyToManyField(User)
    #pStatus = models.BooleanField()
 
    #def count(self):
    #    return len(self.pSell.all())

    def __str__(self):
        return self.pName


class Category(models.Model):
    nameCategory = models.CharField(max_length = 30)

    def  __str__(self):
        return self.nameCategory


class MyFavorite(models.Model):
    pID  = models.CharField(max_length = 30)
    uID  = models.CharField(max_length = 30)
    pName = models.CharField(max_length = 30,blank = True)
    

    def __str__(self):
        return self.pID 