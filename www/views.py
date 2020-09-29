import os

from django.shortcuts import render, HttpResponseRedirect

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from www.forms import ContactForm
from product.forms import SearchForm


def home(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    context["jumbotron_search_form"] = SearchForm(auto_id="jumbotron_%s")
    context["contact_form"] = ContactForm()
    return render(request, "www/home.html", context=context)


def legal_notice(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    return render(request, "www/legal-notice.html", context=context)


def send_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data["from_email"]
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            message = Mail(
                from_email=from_email,
                to_emails='olivier.loustaunau@gmail.com',
                subject=subject,
                html_content=content
            )
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(message)
    return HttpResponseRedirect("/")
