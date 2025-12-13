# Create your models here.
from django.db import models
import datetime
from django.utils import timezone
from urllib.parse import urlparse, parse_qs
import re
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.utils.text import slugify
import uuid

def generate_unique_slug(model_class, value):
    """
    Generates a unique slug for the model based on the title.
    Appends a short UUID if the slug already exists.
    """
    slug = slugify(value)
    unique_slug = slug
    num = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{str(uuid.uuid4())[:8]}"
        num += 1
    return unique_slug


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
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


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
    slug = models.SlugField(unique=True, blank=True)  # ✅ Add slug field
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.location)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        if self.image2:
            self.image2.delete(save=False)
        super().delete(*args, **kwargs)
    
    # on going project


class UpcomingProject(models.Model):
   
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # ✅ Add slug field
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(UpcomingProject, self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Ongoing projects"
    # about page AboutVideo

class AboutVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.video_file:
            self.video_file.delete(save=False)
        super().delete(*args, **kwargs)
    


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
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


# class Video(models.Model):
#     title = models.CharField(max_length=255)
#     video_file = models.FileField(upload_to='testimonals/videos/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
#     class Meta:
#         verbose_name_plural = "video testimonials"


class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "video testimonials"

    @property
    def youtube_id(self):
        """
        Safely extract the YouTube video ID from the youtube_url.
        Returns an empty string if no valid ID found.
        Supports:
         - https://youtu.be/<id>
         - https://www.youtube.com/watch?v=<id>
         - https://www.youtube.com/embed/<id>
         - other common youtube formats
        """
        if not self.youtube_url:
            return ""

        url = self.youtube_url.strip()

        # 1) short youtu.be/ID
        m = re.match(r'https?://youtu\.be/([A-Za-z0-9_-]{11})', url)
        if m:
            return m.group(1)

        # 2) embed or /v/ style
        m = re.search(r'(?:embed/|/v/)([A-Za-z0-9_-]{11})', url)
        if m:
            return m.group(1)

        # 3) normal watch?v=ID
        parsed = urlparse(url)
        if parsed.hostname and 'youtube' in parsed.hostname:
            qs = parse_qs(parsed.query)
            v = qs.get('v')
            if v:
                return v[0]

        # 4) last-chance regex (catch IDs occurring anywhere)
        m = re.search(r'([A-Za-z0-9_-]{11})', url)
        return m.group(1) if m else ""

    
class ProjectVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='projects/videos/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    




# elite_interior/models.py
import re
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


YOUTUBE_ID_RE = re.compile(r"(?:v=|youtu\.be/|embed/)?([A-Za-z0-9_-]{11})")


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_link = models.URLField(
        max_length=500,
        help_text="Paste full YouTube URL or video ID"
    )
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    # 🔹 Normalize input (ID / URL → clean ID)
    def clean(self):
        if not self.youtube_link:
            return

        url = self.youtube_link.strip()
        match = YOUTUBE_ID_RE.search(url)

        if not match:
            raise ValidationError("Invalid YouTube URL or Video ID")

        # Store ONLY the video ID internally
        self.youtube_link = match.group(1)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # ✅ SAME STYLE AS PackageOffers
    def youtube_embed_url(self):
        if not self.youtube_link:
            return ""

        # youtube_link is already normalized to ID
        return f"https://www.youtube.com/embed/{self.youtube_link}"


    
class SliderVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='contact-slider/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.video_file:
            self.video_file.delete(save=False)
        super().delete(*args, **kwargs)


    
class AboutTitleVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='about-head/')  # Stores uploaded videos
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.video_file:
            self.video_file.delete(save=False)
        super().delete(*args, **kwargs)



class SEOServicePage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)   # allow blank and auto-fill
    short_description = models.TextField()
    long_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # auto-generate slug, use underscores instead of hyphens
        if not self.slug:
            base = slugify(self.title)          # e.g. "Top Builders in Trichy" -> "top-builders-in-trichy"
            base = base.replace('-', '_')       # -> "top_builders_in_trichy"
            slug = base
            # ensure uniqueness (append number if needed)
            counter = 1
            while SEOServicePage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}_{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class SEOServiceImage(models.Model):
    page = models.ForeignKey(SEOServicePage, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="seo_pages/")
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.page.title} - Image"

@receiver(post_delete, sender=SEOServiceImage)
def delete_ad_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        instance.image.delete(save=False)