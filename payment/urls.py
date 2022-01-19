from django.urls import path
from .views import payment_canceled, payment_done, PaymentProcess

app_name = "payment"

urlpatterns = [
    path("process/", PaymentProcess.as_view(), name="process"),
    path("done/", payment_done, name="done"),
    path("canceled/", payment_canceled, name="canceled"),
]
