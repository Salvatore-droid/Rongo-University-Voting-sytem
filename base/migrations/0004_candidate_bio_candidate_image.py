# Generated by Django 4.2.19 on 2025-02-25 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_voter_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
