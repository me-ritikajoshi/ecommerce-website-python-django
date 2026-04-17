from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render

from product.models import Category, Order, Product
from userspage.auth import admin_only

# Create your views here.
@login_required
@admin_only
def admin_home(request):
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(delivery_status="Delivered").count()
    total_users = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    out_of_stock_products = Product.objects.filter(stock__lte=0).count()
    total_categories = Category.objects.count()
    total_sales = (
        Order.objects.filter(payment_status=True).aggregate(total=Sum("total_price"))["total"]
        or 0
    )

    context = {
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "total_users": total_users,
        "total_products": total_products,
        "out_of_stock_products": out_of_stock_products,
        "total_categories": total_categories,
        "total_sales": total_sales,
    }
    return render(request, "admins/dashboard.html", context)
