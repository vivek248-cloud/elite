# Create your models here.
from django.db import models
import datetime
from django.utils import timezone


class HomeSlider(models.Model):
    healine = models.CharField(max_length=255)
    sub_headline = models.CharField(max_length=255)
    quotes = models.TextField(blank=True, null=True)  # Optional quotes field
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='home_slider/')

    description = models.TextField(blank=True, null=True)  # Optional description
    location = models.CharField(max_length=255, null=True, blank=True)  # ✅ New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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
    date = models.DateField(default=datetime.date.today)

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

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def project_count(self):
        return self.project_set.count()
    project_count.short_description = 'Projects Count'


# class Project(models.Model):
#     CATEGORY_CHOICES = [
#         ('residential', 'Residential'),
#         ('commercial', 'Commercial'),
#         ('interior', 'interior'),
#     ]
#     title = models.CharField(max_length=255)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     description = models.TextField()
#     image = models.ImageField(upload_to='projects/')
#     # image = CloudinaryField('image',folder='projects-img')
#     location = models.CharField(max_length=255, null=True, blank=True)  # ✅ New field
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     date = models.DateField(default=datetime.date.today)
#     sq_feet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     bhk = models.CharField(max_length=100,null=True, blank=True)
#     budget_range = models.ForeignKey(BudgetRange, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('interior', 'Interior'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='projects-img/')
    image2 = models.ImageField(upload_to='projects-img/', null=True, blank=True)

    location = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    sq_feet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bhk = models.CharField(max_length=100, null=True, blank=True)
    budget_range = models.ForeignKey(BudgetRange, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
    # on going project


class UpcomingProject(models.Model):
   
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='upcomming-project-img/') 
    # image = CloudinaryField('image',folder='upcomming-projects-img')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')  # ✅ NEW FIELD
    location = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sq_feet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bhk = models.CharField(max_length=100,null=True, blank=True)
    budget_range = models.ForeignKey('BudgetRange', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Ongoing projects"
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
    image = models.ImageField(upload_to="teams/")
    author_name = models.CharField(max_length=100)
    author_designation = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='testimonals/videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "video testimonials"
    
class ProjectVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='projects/videos/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(
        max_length=100,
        help_text="Paste the YouTube video ID only (e.g. FT9g4LLrR5c)"
    )
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class SliderVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='contact-slider/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class AboutTitleVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='about-head/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
