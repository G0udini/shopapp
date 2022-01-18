from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import RedirectView
from .models import Coupon
from .forms import CouponApplyForm


class CouponApply(RedirectView):
    url = reverse_lazy("cart:cart_detail")

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                coupon = Coupon.objects.get(
                    code=code, valid_from__lte=now, valid_to__gte=now, active=True
                )
                request.session["coupon_id"] = coupon.id
            except Coupon.DoesNotExist:
                request.session["coupon_id"] = None
        return super().post(self, request, *args, **kwargs)
