

# Create your models here.
from django.db import models
import datetime



class BudgetRange(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Silver, Gold, Platinum
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(
        max_length=50,
        choices=[('Turnkey House Construction', 'Turnkey House Construction'), 
                 ('Commercial', 'Commercial')]
    )
    budget_range = models.ForeignKey(BudgetRange, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    location = models.CharField(max_length=255, null=True, blank=True)  # ✅ New field
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    sq_feet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bhk = models.CharField(max_length=100,null=True, blank=True)
    budget_range = models.ForeignKey(BudgetRange, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # on going project


class UpcomingProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/upcoming/')
    location = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sq_feet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bhk = models.CharField(max_length=100,null=True, blank=True)
    budget_range = models.ForeignKey('BudgetRange', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # about page AboutVideo

class AboutVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.title
    


class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="about_images/")
    author_name = models.CharField(max_length=100)
    author_designation = models.CharField(max_length=100)

    def __str__(self):
        return self.title