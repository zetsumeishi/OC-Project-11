from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
