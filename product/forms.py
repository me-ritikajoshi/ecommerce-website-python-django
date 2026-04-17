from django import forms
from django.forms import ModelForm

from .models import Category, Order, Product

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class CategoryForm(ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

        self.fields["quantity"].widget = forms.NumberInput(attrs={"min": 1})
        if self.product:
            self.fields["quantity"].widget.attrs["max"] = self.product.stock

    class Meta:
        model=Order
        fields=['quantity','contact_no','address','payment_method']

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")

        if self.product and quantity > self.product.stock:
            raise forms.ValidationError(
                f"Only {self.product.stock} item(s) are available in stock."
            )
        return quantity

    def clean_contact_no(self):
        contact_no = self.cleaned_data["contact_no"].strip()
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number should contain digits only.")
        if len(contact_no) < 7:
            raise forms.ValidationError("Contact number is too short.")
        return contact_no

    def clean_address(self):
        address = self.cleaned_data["address"].strip()
        if not address:
            raise forms.ValidationError("Address is required.")
        return address
