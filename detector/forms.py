from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Select Image",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*"
            }
        )
    )