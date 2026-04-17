from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from product.models import Cart, Category, Product


class CartFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="strong-pass-123")
        self.category = Category.objects.create(category_name="Phones")
        self.product = Product.objects.create(
            product_name="Phone",
            product_price=500,
            stock=10,
            product_description="Smartphone",
            category=self.category,
        )

    def test_add_to_cart_requires_login(self):
        response = self.client.get(reverse("userspage:add_to_cart", args=[self.product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("userspage:login"), response.url)

    def test_add_to_cart_creates_single_cart_item(self):
        self.client.login(username="alice", password="strong-pass-123")

        self.client.get(reverse("userspage:add_to_cart", args=[self.product.id]))
        self.client.get(reverse("userspage:add_to_cart", args=[self.product.id]))

        self.assertEqual(Cart.objects.filter(user=self.user, product=self.product).count(), 1)


class AuthPagesTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse("userspage:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("userspage:register"))
        self.assertEqual(response.status_code, 200)
