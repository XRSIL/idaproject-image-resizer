# Generated by Django 3.2.4 on 2021-06-20 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0009_alter_resizedimage_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resizedimage',
            name='name',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='ResizedImage',
        ),
    ]
