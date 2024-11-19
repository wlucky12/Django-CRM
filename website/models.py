from django.db import models

# Create your models here.
class Custom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=50)


    def __str__(self):
        return(f"{self.name}")