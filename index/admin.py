

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
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')

    def changelist_view(self, request, extra_context=None):
        # Get category count for dashboard-style stats
        from django.db.models import Count
        category_count = Project.objects.values('category').annotate(total=Count('id'))
        
        extra_context = extra_context or {}
        extra_context['category_count'] = category_count
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Project,ProjectAdmin)

