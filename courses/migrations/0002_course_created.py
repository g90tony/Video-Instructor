# Generated by Django 3.2.4 on 2021-06-11 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created',
            field=models.DateField(auto_now=True),
        ),
    ]
