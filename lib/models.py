from django.db import models
from django.contrib.auth.models import User

# tracking/models.py
from django.db import models

class TractorSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_area = models.FloatField(default=0)  # in acres
    fuel_used = models.FloatField(default=0)   # in liters
    total_cost = models.FloatField(default=0)  # in INR

class GPSPoint(models.Model):
    session = models.ForeignKey(TractorSession, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(default=0)  # km/h
    timestamp = models.DateTimeField(auto_now_add=True)

class StudentDetails(models.Model):
    username = models.CharField(max_length=130)
    email = models.EmailField(max_length=70, unique=True)
    wallet_balance = models.FloatField(default=5000)
    status = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    updated_by = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'student_details'


class BookDetails(models.Model):
    name=models.CharField(max_length=128)
    book_code=models.IntegerField()
    author_name=models.CharField(max_length=128)
    date=models.DateField()
    status=models.CharField(max_length=128)
    amount=models.IntegerField()
    available_books = models.IntegerField()
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)
    book_img = models.FileField(upload_to='image')

    class Meta:
        db_table = "book_details"


class BookTransferHistory(models.Model): 
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    code = models.IntegerField()  
    book_name = models.CharField(max_length=128)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True) 

    
class UserBookDetails(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    books_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserBookStatus(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
