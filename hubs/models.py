# Imports
from django.contrib.auth.models import User


# Models
class Hub(models.Model):
	name=models.CharField(max_length=100, unique=True)
	create_ts=models.DateTimeField(auto_now_add=True)
	owner=models.ForeignKey('User')
    # meta / secondary info
	description=models.TextField(max_length=1000)
	avatar=models.ForeignKey(Image,null=True,blank=True,on_delete=models.SET_NULL)

# allows users to 'subscribe' to a hub so that it appears on their front page
class Subscribe(models.Model):
	user=models.ForeignKey('User')
	hub=models.ForeignKey('Hub')

# A thread that will contain posts
class Thread(models.Model):
	name=models.CharField(max_length=100, unique=True)
	create_ts=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey('User')
	hub=models.ForeignKey('Hub')

class Post(models.Model):
	user=models.ForeignKey('User')
	thread=models.ForeignKey('Thread')
	create_ts=models.DateTimeField(auto_now_add=True)
	body=models.TextField()