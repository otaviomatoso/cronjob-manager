# Generated by Django 4.1.5 on 2023-03-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronjobs', '0002_file_alter_job_u_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(default='SCHEDULED', max_length=20),
        ),
    ]
