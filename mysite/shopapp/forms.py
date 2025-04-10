from django.forms import ModelForm, ClearableFileInput, FileField, Form
from django.contrib.auth.models import Group

from .models import Product, Order

# class ProductForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = 'name', 'price', 'description', 'discount'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(ModelForm):
    images = MultipleFileField(label="Select files", required=False)

    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"


class CSVImportForm(Form):
    csv_file = FileField()
