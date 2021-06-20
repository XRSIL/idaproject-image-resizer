from django import forms
from .models import Image, ResizedImage


class UploadImageForm(forms.ModelForm):
    url = forms.CharField(max_length=2000, required=False)

    class Meta:
        model = Image
        fields = ['image']


class ResizeImageForm(forms.ModelForm):
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)

    class Meta:
        model = ResizedImage
        fields = ['width', 'height']
