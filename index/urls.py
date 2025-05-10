from django.urls import path
from .views import home, services, about, projects, contact, get_quote,project_details,testimonals,terms,load_more_projects,load_more_upcomming_projects,load_more_projects_videos,load_more_youtube_videos
from .views import category,load_more_projects_category
urlpatterns = [
    path('home/', home, name='home'),
    path('elite/home/<str:category>/', home, name='home_with_category'),
    path('category/<str:category>/', category, name='category'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('projects/<int:project_id>/',project_details,name="projects_details"),
    path('contact/', contact, name='contact'),
    path('get-quote/', get_quote, name='get_quote'),
    path('testimonals/',testimonals, name='testimonals'),
    path('terms&conditions/',terms,name='terms'),
    path('load-more-projects/', load_more_projects, name='load_more_projects'),
    path('load-more-projects-category/', load_more_projects_category, name='load_more_projects_category'),
    path('load-more-upcomming-projects/', load_more_upcomming_projects, name='load_more_upcomming_projects'),
    path('load-more-projects-videos/', load_more_projects_videos, name='load_more_projects_videos'),
    path('load-more-youtube-videos/',load_more_youtube_videos, name='load_more_youtube_videos'),

]
