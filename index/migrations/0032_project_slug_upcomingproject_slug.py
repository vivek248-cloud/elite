from django.db import migrations, models
import index.utils


def populate_slugs(apps, schema_editor):
    Project = apps.get_model('index', 'Project')
    for project in Project.objects.all():
        if not getattr(project, 'slug', None):
            project.slug = index.utils.generate_unique_slug(Project, project.name)
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
        migrations.RunPython(populate_slugs),  # Populate existing projects with slug
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
     
    ]
