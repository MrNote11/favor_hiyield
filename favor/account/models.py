from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class Roles(models.Model):
    roles = models.CharField(max_length=20)
    user = models.ManyToManyField(User, through='Features')
    
    def __str__(self):
        return self.user.username
    
class Features(models.Model):
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    features = models.CharField(max_length=20, null=True, blank=True)

