from django.test import TestCase

from .forms import OrderForm
from .models import Category, Product


class OrderFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name="Laptops")
        self.product = Product.objects.create(
            product_name="Laptop",
            product_price=1200,
            stock=3,
            product_description="Gaming laptop",
            category=self.category,
        )

    def test_order_form_rejects_quantity_above_stock(self):
        form = OrderForm(
            data={
                "quantity": 5,
                "contact_no": "9841234567",
                "address": "Kathmandu",
                "payment_method": "Cash on Delivery",
            },
            product=self.product,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_order_form_rejects_non_numeric_contact(self):
        form = OrderForm(
            data={
                "quantity": 1,
                "contact_no": "abc123",
                "address": "Kathmandu",
                "payment_method": "Cash on Delivery",
            },
            product=self.product,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("contact_no", form.errors)
