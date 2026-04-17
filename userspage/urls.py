from django.urls import path

from .views import (
    EsewaView,
    add_to_cart,
    esewa_verify,
    esewa_verify_v2,
    index,
    logout_user,
    my_order,
    post_order,
    product_details,
    products,
    profile,
    register_user,
    remove_cart,
    show_user_cart_items,
    update_profile,
    user_login,
)

app_name = "userspage"

urlpatterns = [
    path("", index, name="home"),
    path("productdetails/<int:product_id>/", product_details, name="product_details"),
    path("productlist/", products, name="product_list"),
    path("register/", register_user, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", logout_user, name="logout"),
    path("addtocart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", show_user_cart_items, name="cart"),
    path("removecart/<int:cart_id>/", remove_cart, name="remove_cart"),
    path("post-order/<int:product_id>/<int:cart_id>/", post_order, name="post_order"),
    path("esewa-verify-legacy/", esewa_verify, name="esewa_verify_legacy"),
    path("myorder/", my_order, name="my_order"),
    path("esewa-form/", EsewaView.as_view(), name="esewa_form"),
    path("esewaverify/<int:order_id>/<int:cart_id>/", esewa_verify_v2, name="esewa_verify"),
    path("profile/", profile, name="profile"),
    path("updateprofile/", update_profile, name="update_profile"),
]
