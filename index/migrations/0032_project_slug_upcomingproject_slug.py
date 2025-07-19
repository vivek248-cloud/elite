from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slug(model, field_value):
    slug = slugify(field_value)
    unique_slug = slug
    num = 1

    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{num}'
        num += 1

    return unique_slug

def populate_slugs(apps, schema_editor):
    Project = apps.get_model('index', 'Project')
    UpcomingProject = apps.get_model('index', 'UpcomingProject')

    for project in Project.objects.all():
        if not project.slug:
            project.slug = generate_unique_slug(Project, project.title)
            project.save()

    for up in UpcomingProject.objects.all():
        if not hasattr(up, 'slug'):
            continue  # Safety check in case field didn't get added
        if not up.slug:
            up.slug = generate_unique_slug(UpcomingProject, up.title)
            up.save()

class Migration(migrations.Migration):

    dependencies = [
        ('index', '0031_remove_video_video_file_video_youtube_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='upcomingproject',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.RunPython(populate_slugs),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
    ]
