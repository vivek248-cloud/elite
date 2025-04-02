

# Register your models here.
from django.contrib import admin
from .models import QuoteRequest, Project,AboutVideo,BudgetRange,Review,UpcomingProject,GalleryImage,AboutSection

admin.site.register(QuoteRequest)
admin.site.register(Project)
admin.site.register(AboutVideo)
admin.site.register(BudgetRange)
admin.site.register(Review)
admin.site.register(UpcomingProject)
admin.site.register(GalleryImage)
admin.site.register(AboutSection)
admin.site.site_header = "Elite Dream Builders Admin"
admin.site.site_title = "Elite Admin Portal"
admin.site.index_title = "Welcome to Elite Dream Builders Admin Panel"