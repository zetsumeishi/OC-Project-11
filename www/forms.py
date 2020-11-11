from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "email..."}),
        required=True,
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "sujet..."}),
        required=True,
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "message..."}),
        required=True,
    )
