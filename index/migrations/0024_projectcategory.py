# Generated by Django 5.1.7 on 2025-04-17 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_homeslider_healine_homeslider_quotes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
