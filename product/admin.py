from django.contrib import admin
from .models import Cart, Category, Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "product_price", "stock", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("product_name", "product_description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "created_at")
    search_fields = ("category_name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_at")
    list_select_related = ("user", "product")
    search_fields = ("user__username", "product__product_name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "total_price",
        "payment_method",
        "payment_status",
        "delivery_status",
        "created_at",
    )
    list_filter = ("payment_method", "payment_status", "delivery_status", "created_at")
    list_select_related = ("user", "product")
    search_fields = ("user__username", "product__product_name", "contact_no")

