from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from main.models import Product
from main.recommender import Recommender
from coupons.forms import CouponApplyForm
from .cart import Cart
from .forms import CartAddProductForm


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, cd["quantity"], cd["update"])
        return redirect("cart:cart_detail")


class CartDelete(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("cart:cart_detail")


class CartDetail(TemplateView):

    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coupon_apply_form"] = CouponApplyForm()
        context["rcommended_products"] = kwargs.get("recommended_products")
        return context

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "update": True}
            )
        cart.generete_cart()
        r = Recommender()
        cart_products = [item["product"] for item in cart]
        kwargs["recommended_products"] = r.suggest_products_for(
            cart_products, max_results=4
        )
        return super().get(self, request, *args, **kwargs)
