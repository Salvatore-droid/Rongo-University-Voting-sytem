# Generated by Django 4.2.19 on 2025-02-27 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_position_position_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.candidate'),
        ),
    ]
