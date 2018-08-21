from django.db import models
from django import forms
import datetime

# Create your models here.
class Member(models.Model):
	name = models.CharField(max_length=10, null=False)
	gender = models.CharField(max_length=1, null=False,
		choices=(
			('남','남자'),
			('여','여자')
			), default='남'
		)
	birthday = models.DateField(null=False)
	homeplace = models.CharField(max_length=15)
	workplace = models.CharField(max_length=15)
	favorite = models.CharField(max_length=25)
	introduction = models.TextField()
	joindate = models.DateField(default=datetime.date.today, null=False)
	recentdate = models.DateField(default=datetime.date.today, null=False)
	times = models.IntegerField(default=0)
	def __str__(self):
		return self.name