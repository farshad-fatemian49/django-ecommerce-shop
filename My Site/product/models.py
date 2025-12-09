# from distutils.command.upload import upload
from itertools import product
from urllib import request
from django.db import models
from django.forms import CharField, DateTimeField, HiddenInput
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.


# class ImageAlbum(models.Model):
#     def default(self):
#         return self.images.filter(default=True).first()
#     def thumbnails(self):
#         return self.images.filter(width__lt=100, length_lt=100)
    
# class Image(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to="products/%Y/%m/%d/",)
#     default = models.BooleanField(default=False)
#     width = models.FloatField(default=100)
#     length = models.FloatField(default=100)
#     album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)


    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    # album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE)
    # image = models.ImageField(upload_to="products/%Y/%m/%d/",blank=False)
    category = models.ForeignKey("Category",related_name="Products", verbose_name=("دسته بندی"), on_delete=models.CASCADE,blank=True,null=True)
    tags = models.ManyToManyField("Tag",related_name="Products", verbose_name=("تگ") ,blank=True)
    cover = models.ImageField(upload_to="products/%Y/%m/%d/",blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number = models.IntegerField(default=1)
    description = models.TextField(default="Empty",max_length=100)
    seller = models.ForeignKey(get_user_model(),related_name="products",on_delete=models.CASCADE)
    # toptrend = models.ForeignKey("Toptrend",related_name="trends",on_delete=models.PROTECT,blank=True,null=True) 
    
    
    @property
    def dollar_amount(self):
        return "$%s" % self.price if self.price else ""
    
    @property
    def availability(self):
        return "%s" % "Available" if self.available else "Unavailable"
   
    def __str__(self):
        return self.name
    
    
class Comments(models.Model):
    product = models.ForeignKey(Product,related_name="comments", on_delete=models.CASCADE )
    comment = models.TextField(max_length=200)
    writer = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.writer)
    
    
    
class Picture(models.Model):
    picture = models.ImageField(upload_to="products/%Y/%m/%d/",blank=False)
    product = models.ForeignKey(Product,related_name="Pictures", on_delete=models.CASCADE )  

    def __str__(self):
        return self.picture.url
    

class Category(models.Model):
    title = models.CharField(("اسم کتگوری"), max_length=50)
    slug = models.SlugField(("نام انگلیسی"))
    created = models.DateTimeField(("تاریخ ساخته شدن"), auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
class Tag(models.Model):
    title = models.CharField(("اسم تگ"), max_length=50)
    slug = models.SlugField(("نام انگلیسی"))
    created = models.DateTimeField(("تاریخ ساخته شدن"), auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    
class Toptrend(models.Model):
    description = models.TextField(default="خالی",max_length=100)
    new_price = models.PositiveIntegerField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name


    
class Newarrival(models.Model):
    name = models.CharField(max_length=200,default="New Arrivals")
    
    
class Productget(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    trend = models.ForeignKey(Newarrival, verbose_name=(""), related_name="trends", on_delete=models.CASCADE)
    
    
class DiscountedProducts(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    new_price = models.CharField(max_length=5,default=0,blank=True,null=True)
    # percentage = models.CharField(max_length=5,default=0,blank=True,null=True)