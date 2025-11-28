from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib import messages
from .models import Plan, Subscription, Business
from .forms import BusinessForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# TODO: Billing provider integration pending (Stripe, Paddle, etc.)
from datetime import datetime, timedelta, date


def get_user_plan(request):
    user_plan_qs = Subscription.objects.filter(business=request.user.business)
    if user_plan_qs.exists():
        return user_plan_qs.first()
    return None


def get_selected_plan(request):

    plan_type = request.session.get("selected_plan_type")
    host = request.get_host()

    selected_plan_qs = Plan.objects.filter(name=plan_type)
    if selected_plan_qs.exists():
        return selected_plan_qs.first()

    return HttpResponse("Session expire")


def has_expire(request):
    sub = Subscription.objects.get(business=request.user.business)

    return sub.ends_time < timezone.now()


class PricingPage(ListView):
    template_name = "membership/pricing_page.html"
    model = Plan

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            current_plan = get_user_plan(self.request)
            context["current_plan"] = str(current_plan.plan)
        return context

    def post(self, request, *args, **kwargs):
        selected_plan_type = request.POST.get("plan_id")

        user_subscription = get_user_plan(request)

        has_expired = has_expire(request)
        print("has_expire:", has_expired)

        selected_plan_qs = Plan.objects.filter(id=selected_plan_type)

        if selected_plan_qs.exists():
            selected_plan = selected_plan_qs.first()

        # VALIDATION
        if user_subscription.plan == selected_plan:
            if user_subscription != None:
                messages.info(request, "Your have already this plan")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        # ASIGN TO SESSION
        request.session["selected_plan_type"] = selected_plan.name

        return HttpResponseRedirect(reverse("membership:payment"))


@login_required
def paymentView(request):
    """
    Placeholder payment view - billing integration pending.
    Shows placeholder UI indicating billing provider needs to be configured.
    """
    selected_plan = get_selected_plan(request)
    if isinstance(selected_plan, HttpResponse):
        return selected_plan

    # selected_plan is already a Plan object from get_selected_plan
    context = {"plans": selected_plan}
    return render(request, "membership/payment.html", context)


class BusinessUpdateView(UpdateView):
    model = Business
    fields = [
        "name",
        "location",
        "business_type",
        "website",
    ]
    template_name = "membership/business_update.html"
    success_url = reverse_lazy("dashboard")
