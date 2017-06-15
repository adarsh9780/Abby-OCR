from django import forms
from .models import ImageModel

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['imageName', 'image']

    def clean_imageName(self):
        imageName = self.cleaned_data.get('imageName')
        return imageName

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return image