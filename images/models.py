from django.db import models
import hashlib
import random
import os


# Utility Functions
def gen_image_name(instance, filename):
    randomname = hashlib.md5(str(random.randint(0,1000000))).hexdigest()
    fullname = os.path.join("images/full/",randomname)
    try:
        Image.objects.get(photo=fullname)
        return gen_image_name(instance,filename)
    except Image.DoesNotExist:
        return fullname

# Image models
class Image(models.Model):
    image=models.ImageField(upload_to=gen_image_name,blank=False)
    create_ts=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=100,blank=True,unique=True)
    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs) 
        if len(self.name)==0:
            self.name=os.path.basename(self.image.name)
        super(Image, self).save(*args, **kwargs) 
    
    