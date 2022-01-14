from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


class ProductList(TemplateView):
    template_name = "main/product/list.html"

    def get_queryset(self, **kwargs):
        products = Product.objects.filter(available=True)
        category = kwargs.get("category", None)
        if category:
            products = products.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        return {
            "category": kwargs.get("category", None),
            "categories": categories,
            "products": self.queryset,
        }

    def get(self, request, category_slug=None, *args, **kwargs):
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)

        self.queryset = self.get_queryset(category=category)
        context = self.get_context_data(category=category)
        return self.render_to_response(context)


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         language = request.LANGUAGE_CODE
#         category = get_object_or_404(
#             Category,
#             translations__language_code=language,
#             translations__slug=category_slug,
#         )
#         products = products.filter(category=category)
#     context = {
#         "categories": categories,
#         "products": products,
#         "category": category,
#     }
#     return render(request, "main/product/list.html", context)


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "main/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )
