# Generated by Django 3.2 on 2021-07-05 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_main', '0020_removed_entry_api_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='tag',
            field=models.ManyToManyField(blank=True, to='dfirtrack_main.Tag'),
        ),
    ]
