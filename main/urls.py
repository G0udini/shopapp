from django.urls import path
from .views import ProductList, ProductDetail

app_name = "main"
urlpatterns = [
    path(
        "<slug:category_slug>/", ProductList.as_view(), name="product_list_by_category"
    ),
    path("<int:pk>/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("", ProductList.as_view(), name="product_list"),
]
