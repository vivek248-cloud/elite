from django.urls import path
from .views import home, services, about, projects, contact, get_quote,project_details,testimonals,terms

urlpatterns = [
    path('home/', home, name='home'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('projects/<int:project_id>/',project_details,name="projects_details"),
    path('contact/', contact, name='contact'),
    path('get-quote/', get_quote, name='get_quote'),
    path('testimonals/',testimonals, name='testimonals'),
    path('terms & conditions/',terms,name='terms'),
]

