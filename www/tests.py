import os

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from www.forms import ContactForm


class WwwViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse("www:home"))
        self.assertEqual(response.status_code, 200)

    def test_legal_notice(self):
        response = self.client.get(reverse("www:legal-notice"))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


class ContactFormTests(TestCase):
    def test_contact_form(self):
        form_data = {
            "from_email": "olivier.loustaunau@gmail.com",
            "subject": "Test subject",
            "content": "Content of the email."
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        form_data = {"from_email": "not_an_email"}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())


class SendGridTests(TestCase):
    def test_sendgrid(self):
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        message = Mail(
            from_email='olivier.loustaunau@gmail.com',
            to_emails='olivier.loustaunau@gmail.com',
            subject='Sending with Twilio SendGrid is Fun',
            html_content='Test content'
        )
        response = sg.send(message)
        self.assertEqual(response.status_code, 202)
