# Generated by Django 4.2.5 on 2023-10-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(blank=True, help_text='يمكنك الكتابة عن نفسك مثل:مهاراتك وخبراتك ... الخ.', null=True, verbose_name='الوصف'),
        ),
    ]
