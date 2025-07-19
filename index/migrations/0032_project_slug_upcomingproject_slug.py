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
    Project = apps.get_model('index', 'Project')
    for project in Project.objects.all():
        if not project.slug:
            project.slug = generate_unique_slug(Project, project.name)
            project.save()


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
        migrations.RunPython(populate_slugs),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
        migrations.AddField(
            model_name='upcomingproject',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
