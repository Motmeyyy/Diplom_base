# Generated by Django 4.2 on 2023-06-10 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_product_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'managed': False},
        ),
    ]
