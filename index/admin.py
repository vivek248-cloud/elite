# Register your models here.
from django.contrib import admin
from .models import QuoteRequest, Project,AboutVideo,BudgetRange,Review,UpcomingProject,GalleryImage,AboutSection,Video,ProjectVideo,YouTubeVideo,HomeSlider,SliderVideo
from .models import AboutTitleVideo
admin.site.register(QuoteRequest)

admin.site.register(AboutVideo)
admin.site.register(BudgetRange)
admin.site.register(Review)
admin.site.register(UpcomingProject)
admin.site.register(GalleryImage)
admin.site.register(AboutSection)
admin.site.register(Video)
admin.site.register(ProjectVideo)
admin.site.register(YouTubeVideo)
admin.site.register(HomeSlider)
admin.site.register(SliderVideo)
admin.site.register(AboutTitleVideo)

admin.site.site_header = "Elite Dream Builders Admin"
admin.site.site_title = "Elite Admin Portal"
admin.site.index_title = "Welcome to Elite Dream Builders Admin Panel"
from django.contrib import admin
from django.db.models import Count
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'status')
    list_filter = ('category', 'status')
    search_fields = ('title', 'location')
    
    # Fields displayed in the add/edit form
    fields = (
        'title', 'category', 'description',
        'image', 'image2',  # Include both images here
        'location', 'price', 'date',
        'sq_feet', 'bhk', 'budget_range', 'status'
    )

    def changelist_view(self, request, extra_context=None):
        # Get count of projects per category
        category_count = Project.objects.values('category').annotate(total=Count('id'))
        status_count = Project.objects.values('status').annotate(total=Count('id'))

        extra_context = extra_context or {}
        extra_context['category_count'] = category_count
        extra_context['status_count'] = status_count

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Project, ProjectAdmin)

