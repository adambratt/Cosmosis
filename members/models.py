from django.db import models
from django.contrib.auth.models import User
from images.models import Image
from django.db.models.signals import post_save
from django.utils.hashcompat import sha_constructor
from django.conf import settings
import random

##############################
# Universal Classes
##############################

COMMENT_TYPES = (
    ('Area', 'Area'),
    ('Profile', 'Profile'),
    ('Photo', 'Photo'),
)

class Comment(models.Model):
    body=models.TextField()
    member=models.ForeignKey('Member',related_name='member_comment')
    type=models.CharField(max_length=10,blank=True,choices=COMMENT_TYPES)
    create_ts=models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = "create_ts"
        ordering = ["-create_ts"]

##############################
# Member Related Classes
##############################

# Member Class
class Member(models.Model):
    user=models.OneToOneField(User) 
    avatar=models.ForeignKey(Image,null=True,blank=True,on_delete=models.SET_NULL)
    email_verified=models.BooleanField(default=False)
    def __unicode__(self):
        return self.user.username
    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.user.first_name, self.user.last_name)
    def _get_thumb(self):
        if(self.avatar):
            return '/image/'+self.avatar.name+'/thumb/'
        return settings.STATIC_URL+'images/thumb.png'
    full_name=property(_get_full_name)
    thumb=property(_get_thumb)
    

#Signal for creating member profile on user creation
def add_member(sender, instance, created, **kwargs):
    if created:
        member=Member.objects.create(user=instance)
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = instance.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = sha_constructor(salt+username).hexdigest()
        EmailActivation.objects.create(account=instance, activation_key=activation_key)
post_save.connect(add_member, sender=User)

class EmailActivation(models.Model):
    account=models.OneToOneField(User)
    activation_key = models.CharField('Activation Key', max_length=40)
    create_ts=models.DateTimeField(auto_now_add=True)