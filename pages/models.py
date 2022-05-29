from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Review(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class Feature(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    name= models.CharField(max_length=255)
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

