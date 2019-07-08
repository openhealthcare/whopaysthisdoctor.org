from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def send_mail(
    to_emails,
    subject,
    template,
    template_context
):
    template = get_template(template)
    result = template.render(template_context)
    text_content = ''
    msg = EmailMultiAlternatives(
        subject, text_content, settings.DEFAULT_FROM_EMAIL, to_emails
    )
    msg.attach_alternative(result, "text/html")
    msg.send()
