from django import forms

class ImageForm(forms.Form):
    image = forms.ImageField(label='Upload Image')
    # words = forms.CharField(label='Enter range:', max_length=100, required=False)