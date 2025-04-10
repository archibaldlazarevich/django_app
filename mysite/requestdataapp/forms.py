from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class UserBioForms(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label="your age", min_value=1, max_value=120)
    bio = forms.CharField(label="biography", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("File name should not contain `virus`")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
