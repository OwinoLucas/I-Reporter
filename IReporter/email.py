from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to the I Reporter'
    sender = 'lucowish35@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/newsemail.txt',{"first_name": first_name})
    html_content = render_to_string('email/newsemail.html',{"first_name": first_name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()