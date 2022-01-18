from django.urls import path
from .views import CouponApply

app_name = "coupons"

urlpatterns = [
    path("apply/", CouponApply.as_view(), name="apply"),
]
