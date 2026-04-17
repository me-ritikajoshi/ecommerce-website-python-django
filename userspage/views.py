import base64
import hashlib
import hmac
import json
import uuid
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from product.forms import OrderForm
from product.models import Cart, Order, Product

from .auth import unauthenticated_user
from .forms import LoginForm, ProfileUpdateForm


def index(request):
    latest_products = Product.objects.select_related("category").all()[:8]
    context = {
        "products": latest_products,
    }
    return render(request, "users/index.html", context)


def product_details(request, product_id):
    product = get_object_or_404(Product.objects.select_related("category"), id=product_id)
    context = {
        "product": product,
    }
    return render(request, "users/productdetails.html", context)


def products(request):
    product_queryset = Product.objects.select_related("category").all()
    paginator = Paginator(product_queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "users/products.html", context)


@unauthenticated_user
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("userspage:login")

        messages.error(request, "Please verify your details")
        return render(request, "users/register.html", {"forms": form})

    context = {
        "forms": UserCreationForm(),
    }
    return render(request, "users/register.html", context)


@unauthenticated_user
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data["username"],
                password=data["password"],
            )

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("adminpage:dashboard")
                return redirect("userspage:profile")

        messages.error(request, "Please provide valid credentials")
        return render(request, "users/login.html", {"forms": form})

    context = {
        "forms": LoginForm(),
    }
    return render(request, "users/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("userspage:login")


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product, user=user)
    if created:
        messages.success(request, "Product added to the cart")
    else:
        messages.error(request, "Product is already in the cart")

    return redirect("userspage:cart")


@login_required
def show_user_cart_items(request):
    items = Cart.objects.select_related("product").filter(user=request.user)
    context = {
        "items": items,
    }
    return render(request, "users/cart.html", context)


@login_required
def remove_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart.delete()
    messages.success(request, "Item removed from the cart")
    return redirect("userspage:cart")


@login_required
def post_order(request, product_id, cart_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, id=cart_id, user=user, product=product)

    if request.method == "POST":
        form = OrderForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            contact_no = form.cleaned_data["contact_no"]
            address = form.cleaned_data["address"]
            payment_method = form.cleaned_data["payment_method"]

            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product.id)

                if quantity > product.stock:
                    messages.error(request, f"Only {product.stock} item(s) are available.")
                    return render(request, "users/orderform.html", {"forms": form})

                product.stock -= quantity
                product.save(update_fields=["stock"])

                order = Order.objects.create(
                    product=product,
                    user=user,
                    quantity=quantity,
                    total_price=int(quantity * product.product_price),
                    contact_no=contact_no,
                    address=address,
                    payment_method=payment_method,
                    payment_status=payment_method == "Cash on Delivery",
                )

            if order.payment_method == "Cash on Delivery":
                cart_item.delete()
                messages.success(request, "Order placed successfully")
                return redirect("userspage:my_order")

            query_string = urlencode({"o_id": order.id, "c_id": cart_item.id})
            return redirect(f"{reverse('userspage:esewa_form')}?{query_string}")

        messages.error(request, "Please verify your order details")
        return render(request, "users/orderform.html", {"forms": form})

    context = {
        "forms": OrderForm(product=product),
    }
    return render(request, "users/orderform.html", context)


def esewa_verify(request):
    o_id = request.GET.get("pid")
    amount = request.GET.get("amt")
    ref_id = request.GET.get("refId")

    if not all([o_id, amount, ref_id]):
        messages.error(request, "Invalid payment callback data")
        return redirect("userspage:cart")

    try:
        response = requests.post(
            "https://uat.esewa.com.np/epay/transrec",
            {
                "amt": amount,
                "scd": "EPAYTEST",
                "rid": ref_id,
                "pid": o_id,
            },
            timeout=15,
        )
        response.raise_for_status()
        root = ET.fromstring(response.content)
        status = (root[0].text or "").strip().lower()
    except (requests.RequestException, ET.ParseError):
        messages.error(request, "Unable to verify payment with eSewa")
        return redirect("userspage:cart")

    if status == "success":
        try:
            order_id, cart_id = o_id.split("_", 1)
        except ValueError:
            messages.error(request, "Invalid payment reference")
            return redirect("userspage:cart")

        order = get_object_or_404(Order, id=order_id)
        if not order.payment_status:
            order.payment_status = True
            order.save(update_fields=["payment_status"])

        Cart.objects.filter(id=cart_id, user=order.user).delete()
        messages.success(request, "Payment successful")
        return redirect("userspage:my_order")

    messages.error(request, "Unable to complete payment")
    return redirect("userspage:cart")


@login_required
def my_order(request):
    items = Order.objects.select_related("product").filter(user=request.user)
    context = {
        "items": items,
    }
    return render(request, "users/myorder.html", context)


@method_decorator(login_required, name="dispatch")
class EsewaView(View):
    secret_key = "8gBm/:&EnhH.1/q"

    @staticmethod
    def gen_sha256(key, message):
        key = key.encode("utf-8")
        message = message.encode("utf-8")
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        digest = hmac_sha256.digest()
        return base64.b64encode(digest).decode("utf-8")

    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        c_id = request.GET.get("c_id")

        order = get_object_or_404(Order, id=o_id, user=request.user)
        cart = get_object_or_404(Cart, id=c_id, user=request.user)

        uuid_val = uuid.uuid4()
        data_to_sign = (
            f"total_amount={order.total_price},"
            f"transaction_uuid={uuid_val},"
            "product_code=EPAYTEST"
        )
        signature = self.gen_sha256(self.secret_key, data_to_sign)

        success_url = request.build_absolute_uri(
            reverse(
                "userspage:esewa_verify",
                kwargs={"order_id": order.id, "cart_id": cart.id},
            )
        )
        failure_url = request.build_absolute_uri(reverse("userspage:my_order"))

        data = {
            "amount": order.total_price,
            "total_amount": order.total_price,
            "transaction_uuid": uuid_val,
            "product_code": "EPAYTEST",
            "signature": signature,
            "success_url": success_url,
            "failure_url": failure_url,
        }
        context = {
            "order": order,
            "data": data,
            "cart": cart,
        }
        return render(request, "users/esewa.html", context)


@login_required
def esewa_verify_v2(request, order_id, cart_id):
    encoded_data = request.GET.get("data")
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = Cart.objects.filter(id=cart_id, user=request.user).first()

    if not encoded_data:
        messages.error(request, "Missing payment verification payload")
        return redirect("userspage:my_order")

    try:
        padded_data = encoded_data + "=" * (-len(encoded_data) % 4)
        decoded_data = base64.b64decode(padded_data).decode("utf-8")
        map_data = json.loads(decoded_data)
    except (ValueError, json.JSONDecodeError, TypeError):
        messages.error(request, "Invalid payment verification payload")
        return redirect("userspage:my_order")

    if map_data.get("status") == "COMPLETE":
        if not order.payment_status:
            order.payment_status = True
            order.save(update_fields=["payment_status"])

        if cart:
            cart.delete()
        messages.success(request, "Payment successful")
        return redirect("userspage:my_order")

    if not order.payment_status and order.delivery_status != "Payment Failed":
        with transaction.atomic():
            locked_product = Product.objects.select_for_update().get(id=order.product_id)
            locked_product.stock += order.quantity
            locked_product.save(update_fields=["stock"])
            order.delivery_status = "Payment Failed"
            order.save(update_fields=["delivery_status"])

    messages.error(request, "Payment failed")
    return redirect("userspage:my_order")


@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect("userspage:profile")

        messages.error(request, "Failed to update profile")
        return render(request, "users/updateprofile.html", {"forms": form})

    context = {
        "forms": ProfileUpdateForm(instance=request.user),
    }
    return render(request, "users/updateprofile.html", context)


@login_required
def profile(request):
    context = {
        "user": request.user,
    }
    return render(request, "users/profile.html", context)
