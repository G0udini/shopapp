from django.urls import path
from .views import ProductList, product_detail

app_name = "main"
urlpatterns = [
    path("", ProductList.as_view(), name="product_list"),
    path(
        "<slug:category_slug>/", ProductList.as_view(), name="product_list_by_category"
    ),
    path("<int:id>/<slug:slug>/", product_detail, name="product_detail"),
]
