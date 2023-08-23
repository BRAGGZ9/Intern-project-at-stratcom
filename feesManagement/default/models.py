from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=300, default="")
    GENDER_CHOICES = (
        ("MALE","Male"),
        ("FEMALE","Female"),
        ("OTHERS","Others")
    )
    student_number = models.CharField(
        max_length=300, 
        default="hsa/0000/A")
    dob = models.DateField(default=timezone.now)
    nationality = models.CharField(
        max_length=100,
        default="")
    gender = models.CharField(
        max_length=10, 
        default="MALE", 
        choices=GENDER_CHOICES)
    image = models.ImageField(
        upload_to="images/", 
        default="images/pic.png")

    def __str__(self):
        return self.name
    
class Levels(models.Model):
    LEVEL_CHOICES = (
        ("S1","S1"),
        ("S2","S2"),
        ("S3","S3"),
        ("S4","S4"),
        ("S5","S5"),
        ("S6","S6")
    )
    STREAM_CHOICES = (
        ("A","a"),
        ("B","b"),
        ("C","c"),
        ("D","d")
    )
    name = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    stream = models.CharField(max_length=1,choices=STREAM_CHOICES)
    tuition_amount = models.FloatField(default=10000.0)

    def __str__(self):
        return str(self.name + self.stream)
    
class AmountPaid(models.Model):
    student = models.ForeignKey(
        Students,on_delete=models.CASCADE)
    level = models.ForeignKey(
        Levels, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)
    

class PasswordResets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField(null=False, blank=False)
    link = models.CharField(null=False, blank=False, max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("MALE","Male"),
        ("FEMALE","Female")
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(default="MALE", max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    dob = models.DateField(default=timezone.now)
    contact = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.owner)
    
    