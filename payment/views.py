from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.views import View
from django.urls import reverse
from orders.models import Order

import weasyprint
import braintree
from io import BytesIO


class PaymentProcess(View):
    template_name = "payment/process.html"

    def get_order(self, request, *args, **kwargs):
        order_id = request.session.get("order_id")
        return get_object_or_404(Order, id=order_id)

    def get(self, request, *args, **kwargs):
        order = self.get_order(request)
        client_token = braintree.ClientToken.generate()
        context = {
            "order": order,
            "client_token": client_token,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order = self.get_order(request)
        nonce = request.POST.get("payment_method_nonce", None)
        result = braintree.Transaction.sale(
            {
                "amount": "{:.2f}".format(order.get_total_cost()),
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            subject = f"Shop - Invoice no. {order.id}"
            message = "Please, find attached the invoice for your recent purchase."
            email = EmailMessage(subject, message, "admin@shop.com", [order.email])
            html = render_to_string("orders/order/pdf.html", {"order": order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.PDF_ROOT)]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            email.attach(f"order_{order.id}.pdf", out.getvalue(), "applicaation/pdf")
            email.send()
            return redirect(reverse("payment:done"))
        else:
            return redirect(reverse("payment:canceled"))


def payment_done(request):
    return render(request, "payment/done.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
