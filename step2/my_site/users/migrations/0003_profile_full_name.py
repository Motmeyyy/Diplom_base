# Generated by Django 4.2 on 2023-05-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_verificationrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
