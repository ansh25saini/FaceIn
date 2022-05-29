from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
	
class Present(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateField(default=datetime.date.today)
	present=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)
			
class Time(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateField(default=datetime.date.today)
	time=models.DateTimeField(null=True,blank=True)
	out=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)
		