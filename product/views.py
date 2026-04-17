from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from userspage.auth import admin_only

from .forms import CategoryForm, ProductForm
from .models import Category, Product


@login_required
@admin_only
def index(request):
    products = Product.objects.select_related("category").all()
    context = {
        "products": products,
    }
    return render(request, "product/index.html", context)


@login_required
@admin_only
def post_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added")
            return redirect("product:add_product")

        messages.error(request, "Please verify form fields")
        return render(request, "product/addproduct.html", {"forms": form})

    context = {
        "forms": ProductForm(),
    }
    return render(request, "product/addproduct.html", context)


@login_required
@admin_only
def post_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added")
            return redirect("product:add_category")

        messages.error(request, "Please verify form fields")
        return render(request, "product/addcategory.html", {"forms": form})

    context = {
        "forms": CategoryForm(),
    }
    return render(request, "product/addcategory.html", context)


@login_required
@admin_only
def show_category(request):
    category = Category.objects.all()
    context = {
        "category": category,
    }
    return render(request, "product/showcategory.html", context)


@login_required
@admin_only
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect("product:show_category")


@login_required
@admin_only
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted")
    return redirect("product:index")


@login_required
@admin_only
def update_category(request, category_id):
    instance = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated")
            return redirect("product:show_category")

        messages.error(request, "Please verify form fields")
        return render(request, "product/updatecategory.html", {"forms": form})

    context = {
        "forms": CategoryForm(instance=instance),
    }
    return render(request, "product/updatecategory.html", context)


@login_required
@admin_only
def update_product(request, product_id):
    instance = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated")
            return redirect("product:index")

        messages.error(request, "Please verify form fields")
        return render(request, "product/updateproduct.html", {"forms": form})

    context = {
        "forms": ProductForm(instance=instance),
    }
    return render(request, "product/updateproduct.html", context)
