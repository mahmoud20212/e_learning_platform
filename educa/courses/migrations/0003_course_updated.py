# Generated by Django 4.2.5 on 2023-10-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
