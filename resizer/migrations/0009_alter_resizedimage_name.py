# Generated by Django 3.2.4 on 2021-06-19 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0008_rename_resized_image_resizedimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resizedimage',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resizer.image'),
        ),
    ]
