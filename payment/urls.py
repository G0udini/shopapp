from django.urls import path
from .views import payment_canceled, payment_done, payment_process
from django.utils.translation import ugettext_lazy as _

app_name = "payment"

urlpatterns = [
    path(_("process/"), payment_process, name="process"),
    path(_("done/"), payment_done, name="done"),
    path(_("canceled/"), payment_canceled, name="canceled"),
]
