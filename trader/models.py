from django.db import models
from PIL import Image
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg',upload_to='profile_pics') #Field for profile pic.

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
    pName = models.CharField(max_length = 30)
    owner = models.ManyToManyField(User,blank = True)
    ownerName = models.CharField(max_length = 30,blank = True)
    #pDetail = models.TextField(null = True , blank = True)
    #pSell = models.ManyToManyField(User)
    #pStatus = models.BooleanField()
 
    #def count(self):
    #    return len(self.pSell.all())

    def __str__(self):
        return self.pName

