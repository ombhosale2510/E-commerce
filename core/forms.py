from django import forms

PAYMENT_CHOICES = (
    ('P', 'PayPal'),
    ('G', 'Gpay'),
)


class CheckoutForm(forms.Form):
    f_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First name'
    }))
    l_name = forms.CharField()
    street_address = forms.CharField()
    apt_address = forms.CharField(required=False)
    country = forms.CharField()
    state = forms.CharField()
    zip = forms.CharField()
    same_bil_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())

    payment_opt = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
