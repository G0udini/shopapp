from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from cart.cart import Cart
from main.recommender import Recommender
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created

import weasyprint


class OrderCreate(View):

    template_name = "orders/order/create.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.generete_cart()
        form = OrderCreateForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        r = Recommender()
        cart.generete_cart()
        cart.find_coupon()
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            recommend_items = []
            order_items = []
            for item in cart:
                order_items.append(
                    OrderItem(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                )
                recommend_items.append(item["product"])
            OrderItem.objects.bulk_create(order_items)
            r.products_bought(recommend_items)
            cart.clear()
            order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse("payment:process"))
        else:
            return redirect(reverse("orders:order_create"))


class AdminOrderDetail(PermissionRequiredMixin, View):
    permission_required = "is_staff"
    template_name = "admin/orders/order/detail.html"

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(
            Order.objects.prefetch_related("items", "items__product"),
            id=order_id,
        )
        return render(request, self.template_name, {"order": order})


class AdminOrderPDF(PermissionRequiredMixin, View):
    permission_required = "is_staff"

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        html = render_to_string("orders/order/pdf.html", {"order": order})
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"filename='order_{order.id}.pdf'"
        weasyprint.HTML(string=html).write_pdf(
            response, stylesheets=[weasyprint.CSS(settings.PDF_ROOT)]
        )
        return response
