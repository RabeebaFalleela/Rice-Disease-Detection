from django.db import models

# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    farmer=models.CharField(max_length=30)

class getintouch(models.Model):
    SERVICE_CHOICE=(
        ('service 1','SERVICE 1'),
        ('service 2','SERVICE 2'),
    )
    name=models.CharField(max_length=30)
    phone=models.IntegerField()
    email=models.CharField(max_length=30)
    message=models.TextField(max_length=300)
    service=models.CharField(max_length=200,choices=SERVICE_CHOICE)

class UploadImage(models.Model):
    image=models.ImageField(upload_to='infectplants/')

    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"