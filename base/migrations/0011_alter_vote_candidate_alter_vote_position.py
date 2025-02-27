# Generated by Django 4.2.19 on 2025-02-27 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_voter_candidate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.candidate'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.position'),
        ),
    ]
