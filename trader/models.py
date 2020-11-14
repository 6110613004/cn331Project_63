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
    image = models.ImageField(default = 'default.jpg',upload_to='profile_pics') #Field for profile pic.
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
    place1 = models.CharField(max_length=999,blank=True) #สถานที่นัดรับสินค้า:1
    place2 = models.CharField(max_length=999,blank=True) #สถานที่นัดรับสินค้า:2
    place3 = models.CharField(max_length=999,blank=True) #สถานที่นัดรับสินค้า:3
    day1 = models.CharField(max_length=10,blank=True) #วันที่นัดรับสินค้า:1
    day2 = models.CharField(max_length=10,blank=True) #วันที่นัดรับสินค้า:2
    day3 = models.CharField(max_length=10,blank=True) #วันที่นัดรับสินค้า:3
    time1 = models.CharField(max_length=5,blank=True) #เวลาที่นัดรับสินค้า:1
    time2 = models.CharField(max_length=5,blank=True) #เวลาที่นัดรับสินค้า:2
    time3 = models.CharField(max_length=5,blank=True) #เวลาที่นัดรับสินค้า:3
    s1 = models.BooleanField(default = False)
    s2 = models.BooleanField(default = False)
    s3 = models.BooleanField(default = False)

    
   
    
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

Day = (
    'อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์','เสาร์'
)

Time = (
    '00:00','00:30','01:00','01:30','02:00','03:30',
    '04:00','04:30','05:00','05:30','06:00','06:30',
    '07:00','07:30','08:00','08:30','09:00','09:30',
    '10:00','10:30','11:00','11:30','12:00','13:30',
    '14:00','14:30','15:00','15:30','16:00','16:30',
    '17:00','17:30','18:00','18:30','19:00','19:30',
    '20:00','20:30','21:00','21:30','22:00','23:30',
)

place = (
    'ศูนย์การเรียนรู้ กรมหลวงนราธิวาสราชนครินทร์(ศกร)',
    'หอสมุดป๋วย',
    'อาคารเรียนรวมสังคมศาสตร์(SC)',
    'ตึกอาคารเรียนรวมเเละบริหาร1',
    'ตึกอาคารเรียนรวมเเละบริหาร2',
    'ตึกอาคารเรียนรวมเเละบริหาร3',
    'ตึกอาคารเรียนรวมเเละบริหาร4',
    'ตึกอาคารเรียนรวมเเละบริหาร5',
    'ตึกคณะวิศวกรรมศาสตร์',
    'ตึกคณะนิติศาสตร์',
    'ตึกคณะพาณิชยศาสตร์และการบัญชี',
    'ตึกคณะรัฐศาสตร์',
    'ตึกคณะเศรษฐศาสตร์',
    'ตึกคณะสังคมสงเคราะห์ศาสตร์',
    'ตึกคณะสังคมวิทยาและมานุษยวิทยา',
    'ตึกคณะศิลปศาสตร์',
    'ตึกคณะวารสารศาสตร์และสื่อสารมวลชน',
    'ตึกคณะวิทยาศาสตร์และเทคโนโลยี',
    'ตึกคณะสถาบันเทคโนโลยีนานาชาติสิรินธร',
    'ตึกคณะสถาปัตยกรรมศาสตร์และการผังเมือง',
    'ตึกคณะศิลปกรรมศาสตร์',
    'ตึกคณะแพทยศาสตร์',
    'ตึกคณะสหเวชศาสตร์',
    'ตึกคณะทันตแพทยศาสตร์',
    'ตึกคณะพยาบาลศาสตร์',
    'ตึกคณะสาธารณสุขศาสตร์',
    'ตึกคณะเภสัชศาสตร์',
    'ตึกคณะวิทยาการเรียนรู้และศึกษาศาสตร์',
    'ตึกวิทยาลัยพัฒนศาสตร์ ป๋วย อึ๊งภากรณ์',
    'ตึกวิทยาลัยนวัตกรรม',
    'ตึกวิทยาลัยสหวิทยาการ',
    'ตึกวิทยาลัยนานาชาติ ปรีดี พนมยงค์',
    'ตึกวิทยาลัยแพทยศาสตร์นานาชาติจุฬาภรณ์',
    'ตึกวิทยาลัยโลกคดีศึกษา',
    'ตึกสถาบันภาษา',
    'ตึกSIIT',
    'โรงอาหารJC',
    'โรงอาหารกลาง',
    'โรงอาหารบร5',
    'โรงอาหารวิศวกรรมศาสตร์',
    'หอพักโซน B',
    'หอพักโซน C',
    'หอพักโซน E',
    'หอพักโซน M',
    'หอพักโซน F',
    'หอพักเเพทย์',
    'อินเตอร์โซน',
    'AIT',
    'โรงพยาบาลธรรมศาสตร์',
    'ทิวสนโดม',
    'ท่ารถตู้ มธ',
    'ประตูเชียงราก1',
    'ประตูเชียงราก2'
)