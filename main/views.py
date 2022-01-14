from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender


class ProductList(TemplateView):
    template_name = "main/product/list.html"

    def get_queryset(self, **kwargs):
        products = Product.objects.filter(available=True)
        category = kwargs.get("category")
        if category:
            products = products.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        return {
            "category": kwargs.get("category"),
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


class ProductDetail(DetailView):
    template_name = "main/product/detail.html"
    queryset = Product.objects.filter(available=True)
    query_pk_and_slug = True
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = Recommender()
        context["cart_product_form"] = CartAddProductForm()
        context["recommended_products"] = r.suggest_products_for(
            [kwargs.get("object")], 4
        )
        return context
