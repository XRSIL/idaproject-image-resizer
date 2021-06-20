from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Image, ResizedImage
from .forms import UploadImageForm, ResizeImageForm

from PIL import Image as Picture
from urllib.parse import urlencode

import requests
import io
import validators
import os


def main(request):
    context = {
        'images': Image.objects.all()
    }
    return render(request, 'resizer/index.html', context)


# Метод добавляет параметр с названием изображения в URL адрес, для открытия страницы изменения размера
def get_resize_view_url(name):
    query_string = urlencode({'image_name': name})
    base_url = reverse('resize-view')
    url = '{}?{}'.format(base_url, query_string)
    return url


def upload_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():

            # Кейс 1 - указана и ссылка, и сам файл
            if form.data['url'] and form.instance.image.name != 'None':
                messages.error(request, f'Фото не добавлено, указаны два источника изображения')
                return redirect('upload-view')

            # Кейс 2 - не указана ни ссылка, ни файл
            if not form.data['url'] and form.instance.image.name == 'None':
                messages.error(request, f'Фото не добавлено, оба поля пустые')
                return redirect('upload-view')

            # Кейс 3 указана только ссылка
            if form.data['url']:

                # Получаем названия картинки из ссылки
                form.instance.name = str(form.data['url']).split('/')[-1]
                if Image.objects.filter(name=form.instance.name).count() > 0:
                    messages.error(request, 'Картинка с таким именем уже существует')
                    return redirect('upload-view')

                form.instance.image = form.data['url']

                # Проверяем ссылку, ведет ли она к изображению, если да - сохраняем на сервер и добавляем в БД
                if validators.url(form.data['url']):
                    img_url = requests.get(form.data['url'])
                    try:
                        image = Picture.open(io.BytesIO(img_url.content))
                        image.save(f'{os.getcwd()}/media/uploaded_images/{form.instance.name}')
                        form.instance.image = f'uploaded_images/{form.instance.name}'
                    except Picture.UnidentifiedImageError:
                        messages.error(request, 'Указанная ссылка не является изображением')
                        return redirect('upload-view')

                if not validators.url(form.data['url']):
                    messages.error(request, 'Указанная ссылка не является изображением')
                    return redirect('upload-view')
                form.save()

                return redirect(get_resize_view_url(form.instance.name))

            # Кейс 4 указан файл с изображением
            if form.instance.image:
                form.instance.name = form.instance.image.name
                if Image.objects.filter(name=form.instance.name).count() > 0:
                    messages.error(request, 'Картинка с таким именем уже существует')
                    return redirect('upload-view')
                form.save()

                return redirect(get_resize_view_url(form.instance.name))

        if not form.is_valid():
            return redirect('image-form')
    else:
        form = UploadImageForm()

    return render(request, 'resizer/upload_view.html', {'image_form': form})


def resize_view(request):
    # Берем название изображения из URL адреса страницы
    image_name = request.GET.get('image_name')

    url = get_resize_view_url(image_name)

    image_instance = Image.objects.get(name=image_name)

    if ResizedImage.objects.filter(name__name=image_name).count() == 1:
        image_instance = ResizedImage.objects.get(name__name=image_name)

    primary_image = image_instance.image

    image = Picture.open(primary_image)

    if request.method == 'POST':
        form = ResizeImageForm(request.POST, request.FILES)

        if form.is_valid():
            # Кейс 1 - не указана ни ширина, ни высота
            if not form.data['width'] and not form.data['height']:
                messages.error(request, 'Высота и ширина изображения не указаны')
                return redirect(url)

            # Кейс 2 - указана только ширина
            if form.data['width']:
                image_instance = Image.objects.get(name=image_name)

                new_width = int(form.data['width'])
                height = new_width * image.height / image.width

                resized_image = image.resize([new_width, int(height)], Picture.ANTIALIAS)
                form.instance.name = image_instance

                resized_image.save(f'{os.getcwd()}/media/resized_images/{image_instance.name}')
                form.instance.image = f'resized_images/{image_instance.name}'
                if ResizedImage.objects.filter(name__name=image_name).count() == 1:
                    ResizedImage.objects.get(name__name=image_name).delete()
                form.save()
                return redirect(url)

            # Кейс 2 - указана только высота
            if form.data['height']:
                image_instance = Image.objects.get(name=image_name)
                new_height = int(form.data['height'])
                width = new_height * image.width / image.height
                resized_image = image.resize([int(width), new_height], Picture.ANTIALIAS)
                form.instance.name = image_instance

                resized_image.save(f'{os.getcwd()}/media/resized_images/{image_instance.name}')
                form.instance.image = f'resized_images/{image_instance.name}'
                if ResizedImage.objects.filter(name__name=image_name).count() == 1:
                    ResizedImage.objects.get(name__name=image_name).delete()
                form.save()
                return redirect(url)

    else:
        form = ResizeImageForm()

    context = {
        'image_name': image_name,
        'resize_form': form,
        'width': image.width,
        'height': image.height,
        'resized_image': image_instance.image
    }
    return render(request, 'resizer/resize_view.html', context)
