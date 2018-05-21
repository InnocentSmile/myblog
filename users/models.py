from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称',max_length=64)
    headshot = models.ImageField(upload_to='avatar/%Y/%m/%d',default='default.jpg',verbose_name='头像',null=True,blank=True)
    signature = models.CharField(max_length=128,default='this  guy is too lazy to leave anything here.',verbose_name='个性签名',null=True,blank=True)
    class Meta(AbstractUser.Meta):
        pass