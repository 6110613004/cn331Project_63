from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    #ID = models.IntegerField()
    pName = models.CharField(max_length = 30)
    #pDetail = models.TextField(null = True , blank = True)
    #pSell = models.ManyToManyField(User)
    #pStatus = models.BooleanField()
 
    #def count(self):
    #    return len(self.pSell.all())

    def __str__(self):
        return self.pName