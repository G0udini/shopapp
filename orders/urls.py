from django.urls import path
from .views import OrderCreate, AdminOrderDetail, AdminOrderPDF

app_name = "orders"

urlpatterns = [
    path(
        "admin/order/<int:order_id>/pdf/",
        AdminOrderPDF.as_view(),
        name="admin_order_pdf",
    ),
    path(
        "admin/order/<int:order_id>/'",
        AdminOrderDetail.as_view(),
        name="admin_order_detail",
    ),
    path("create/", OrderCreate.as_view(), name="order_create"),
]
