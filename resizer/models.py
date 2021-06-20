from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='uploaded_images', default='None')

    def __str__(self):
        return f'{self.name}'


class ResizedImage(models.Model):
    name = models.OneToOneField(Image, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resized_images')

    def __str__(self):
        return f'{self.name}'
