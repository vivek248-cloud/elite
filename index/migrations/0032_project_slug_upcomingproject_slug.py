from django.db import migrations, models
from django.utils.text import slugify


def generate_unique_slug(model, value):
    base_slug = slugify(value)
    slug = base_slug
    num = 1
    while model.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{num}'
        num += 1
    return slug


def populate_slugs(apps, schema_editor):
    from index.utils import generate_unique_slug  # Import inside the function
    Project = apps.get_model('index', 'Project')
    for project in Project.objects.all():
        if project.title and not project.slug:
            project.slug = generate_unique_slug(Project, project.title)
            project.save()



class Migration(migrations.Migration):

    dependencies = [
        ('index', '0031_remove_video_video_file_video_youtube_url'),
    ]

    operations = [
     
        migrations.RunPython(populate_slugs),
   
        migrations.AddField(
            model_name='upcomingproject',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
