from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    # Quantity of items to add to the cart 
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # Override quantity, this input is hidden from the user 
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)