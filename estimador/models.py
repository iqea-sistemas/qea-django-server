from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IqeaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True  )
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Projects(models.Model):
    user = models.ForeignKey(IqeaUser, on_delete=models.CASCADE, null=True, blank=True )
    project_name= models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    start_date=models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
