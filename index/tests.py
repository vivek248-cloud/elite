# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Project
from .models import AboutVideo
from .models import Review,AboutSection
from .models import UpcomingProject,GalleryImage

class BasicTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))  # Change 'home' to your actual homepage URL name
        self.assertEqual(response.status_code, 200)  # Expecting a successful response



class YourModelTests(TestCase):
    def test_create_object(self):
        obj = Project.objects.create(title="Test")
        self.assertEqual(obj.title, "Test")


class YourModelTests2(TestCase):
    def test_create_object(self):
        obj = AboutVideo.objects.create(title="Test")
        self.assertEqual(obj.title, "Test")

class YourModelTests3(TestCase):
    def test_create_object(self):
        obj = AboutSection.objects.create(title="Test")
        self.assertEqual(obj.title, "Test")

class YourModelTests4(TestCase):
    def test_create_object(self):
        obj = Review.objects.create(name="Test")
        self.assertEqual(obj.name, "Test")

class YourModelTests5(TestCase):
    def test_create_object(self):
        obj = UpcomingProject.objects.create(title="Test")
        self.assertEqual(obj.title, "Test")

class YourModelTests6(TestCase):
    def test_create_object(self):
        obj = GalleryImage.objects.create(title="Test")
        self.assertEqual(obj.title, "Test")
