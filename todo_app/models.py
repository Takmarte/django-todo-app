from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcategories')
 
    def __str__(self):
        prefix = f"{self.parent} > " if self.parent else ""
        return f"{prefix}{self.name}"
    
class Todos(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(max_length=1000,blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now,blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_private = models.BooleanField(default=True)


