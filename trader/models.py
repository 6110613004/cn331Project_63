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
    pName = models.CharField(max_length = 30)                                        # Field ที่เก็บค่า ชื่อของสินค้า
    ownerName = models.CharField(max_length = 30,blank = True)                       # Field ที่เก็บค่า เจ้าของของสินค้า
    ownerID = models.CharField(max_length = 30,blank = True)                         # Field ที่เก็บค่า pk ของเจ้าของสินค้า
    category = models.CharField( max_length=30,blank = True)                         # Field ที่เก็บค่า หมวดหมู่ของสินค้า
    p_image = models.ImageField(upload_to='product_pics',default = 'dafault1.jpg')   # Field ที่เก็บค่า 
    p_detail = models.CharField(max_length = 200,blank = True)                       # Field ที่เก็บค่า รายละเอียดของสินค้า
    p_price = models.CharField(max_length = 6,default = 0)                           # Field ที่เก็บค่า ราคาของสินค้า
    pStatus = models.BooleanField(default = True)                                    # Field ที่เก็บค่า สถานะของสินค้า (True คือ ยังสามารถทำการซื้อขายได้อยู่ False ไม่สามารถทำการซื้อขายได้เเล้ว(สินค้าได้ขายไปแล้ว) )
    MyFavorite = models.ManyToManyField(User,blank = True)                           # Field ที่เก็บค่า คนที่ถูกใจสินค้า (เป็น ManyToMany field)
    place1 = models.CharField(max_length=999,blank=True)                             # Field ที่เก็บค่า สถานที่ที่ 1 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    place2 = models.CharField(max_length=999,blank=True)                             # Field ที่เก็บค่า สถานที่ที่ 2 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    place3 = models.CharField(max_length=999,blank=True)                             # Field ที่เก็บค่า สถานที่ที่ 3 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    day1 = models.CharField(max_length=10,blank=True)                                # Field ที่เก็บค่า วันที่ 1 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    day2 = models.CharField(max_length=10,blank=True)                                # Field ที่เก็บค่า วันที่ 2 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    day3 = models.CharField(max_length=10,blank=True)                                # Field ที่เก็บค่า วันที่ 3 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    time1 = models.CharField(max_length=5,blank=True)                                # Field ที่เก็บค่า เวลาที่ 1 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    time2 = models.CharField(max_length=5,blank=True)                                # Field ที่เก็บค่า เวลาที่ 2 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    time3 = models.CharField(max_length=5,blank=True)                                # Field ที่เก็บค่า เวลาที่ 3 สำหรับการซื้อขาย(เพิ่มโดยผู้ขาย)
    s1 = models.BooleanField(default = False)                                        # Field ที่เก็บค่า ว่าสถานที่ วันที่ และเวลา ที่ 1 ได้ถูกเพิ่มเเล้ว (False = ยังไม่มีข้อมูล ,True = มีข้อมูลแล้ว)
    s2 = models.BooleanField(default = False)                                        # Field ที่เก็บค่า ว่าสถานที่ วันที่ และเวลา ที่ 2 ได้ถูกเพิ่มเเล้ว (False = ยังไม่มีข้อมูล ,True = มีข้อมูลแล้ว)
    s3 = models.BooleanField(default = False)                                        # Field ที่เก็บค่า ว่าสถานที่ วันที่ และเวลา ที่ 3 ได้ถูกเพิ่มเเล้ว (False = ยังไม่มีข้อมูล ,True = มีข้อมูลแล้ว)
    buyerID = models.CharField(max_length = 30,blank = True,default="")              # Field ที่เก็บค่า pk ของผู้ซื้อ
    buyerName = models.CharField(max_length = 30,blank = True,default="")            # Field ที่เก็บค่า ชื่อ ของผู้ซื้อ
    dealplace = models.CharField(max_length=999,blank=True,default="")               # Field ที่เก็บค่า สถานที่ ที่ทำการซื้อขาย
    dealday = models.CharField(max_length=10,blank=True,default="")                  # Field ที่เก็บค่า วัน ที่ทำการซื้อขาย
    dealtime = models.CharField(max_length=5,blank=True,default="")                  # Field ที่เก็บค่า เวลา ที่ทำการซื้อขาย

   
    
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


class Category(models.Model): # ไม่ได้ใช้
    
    nameCategory = models.CharField(max_length = 30)

    def  __str__(self):
        return self.nameCategory




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

CATEGORY_CHOICES = (
    'Books',
    'Accessories',
    'Other',
    'Equipment'
)