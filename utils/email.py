"""
Email Mixin for sending the email
"""

from django.core.mail import EmailMessage
from django.template import loader
from django.conf import settings


class EmailMixin(object):
    """ EmailMixin to send the mail to user  """
    name = None
    subject_template_name = None
    html_body_template_name = None

    def send_email(self, user, **ctx):
        """ send mail """
        subject = loader.render_to_string(self.subject_template_name, ctx)
        subject = ''.join(subject.splitlines())
        html_body = loader.render_to_string(self.html_body_template_name, ctx)

        email_message = EmailMessage(
            subject,
            html_body,
            settings.DEFAULT_FROM_EMAIL,
            [user],
            cc=[]
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
