# Generated by Django 3.1.4 on 2020-12-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0007_remove_mobile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
    ]
