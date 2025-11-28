from django import forms

from .models import Payment, Business


class PaymentForm(forms.ModelForm):
    """
    Payment form - placeholder for future billing integration.
    """

    class Meta:
        model = Payment
        fields = ["phone"]

    # TODO: Add validation for billing provider when integrated


class BusinessForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = [
            "name",
            "location",
        ]
