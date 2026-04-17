from django.urls import path

from .views import (
    delete_category,
    delete_product,
    index,
    post_category,
    post_product,
    show_category,
    update_category,
    update_product,
)

app_name = "product"

urlpatterns = [
    path("", index, name="index"),
    path("addproduct/", post_product, name="add_product"),
    path("addcategory/", post_category, name="add_category"),
    path("showcategory/", show_category, name="show_category"),
    path("deletecategory/<int:category_id>/", delete_category, name="delete_category"),
    path("deleteproduct/<int:product_id>/", delete_product, name="delete_product"),
    path("updatecategory/<int:category_id>/", update_category, name="update_category"),
    path("updateproduct/<int:product_id>/", update_product, name="update_product"),
]
