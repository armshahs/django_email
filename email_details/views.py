from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Email
from .serializers import EmailSerializer
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import transaction

# added for html email including EmailMultiAlternatives added above.
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# passing variables inside the HTML email template
from django.contrib.auth.models import User


# Create your views here.


# Get all your emails from db
@api_view(["GET"])
def get_email(request):
    queryset = Email.objects.all()

    serializer = EmailSerializer(queryset, many=True)
    return Response(serializer.data)
    # return Response({"Message": "Success"})


# Create a new email object, does NOT include sending emails.
@api_view(["POST"])
def create_email(request):
    email = Email.objects.create(
        subject=request.data.get("subject"),
        body=request.data.get("body"),
        email=request.data.get("email"),
    )

    serializer = EmailSerializer(email)
    return Response(serializer.data)
    # return Response({"Message": "Success"})


# Create and send a new TEXT email.
@api_view(["POST"])
@transaction.atomic
def create_send_email(request):

    subject = request.data.get("subject")
    body = request.data.get("body")
    get_email = request.data.get("email")

    email = Email.objects.create(
        subject=subject,
        body=body,
        email=get_email,
    )

    send_mail(
        subject=subject,
        message=body,
        from_email=None,
        recipient_list=[get_email],
        fail_silently=False,
    )

    # serializer = EmailSerializer(email)
    # return Response(serializer.data)
    return Response({"Message": "Success"})


# Create and send a new HTML email
@api_view(["POST"])
def create_send_htmlemail(request):

    subject = request.data.get("subject")
    get_email = request.data.get("email")

    html_message = render_to_string("content/email.html")
    # extracts plain text from html message without the tags.
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=None,
        to=[get_email],
    )

    message.attach_alternative(html_message, "text/html")
    message.send()

    email = Email.objects.create(
        subject=subject,
        body="Email sent",
        email=get_email,
    )

    # serializer = EmailSerializer(email)
    # return Response(serializer.data)
    return Response({"Message": "Success"})


# Create and send a new HTML email by passing variables.
@api_view(["POST"])
def create_send_htmlemail_variables(request):

    subject = request.data.get("subject")
    get_email = request.data.get("email")

    # Adding below code to pass variables.
    # Note: exists only works with filter.
    if User.objects.filter(email=get_email).exists():
        user = User.objects.get(email=get_email)
        welcome_message = "Welcome " + str(user.first_name) + " " + str(user.last_name)
    else:
        welcome_message = "Welcome to our email"

    link_app = "http://127.0.0.1:8000"

    context = {
        "welcome_message": welcome_message,
        "link_app": link_app,
    }

    # pass the context containing the welcome_message and the link_app to the html_message.
    # Also add link_app and welcome_message to the email.html file
    html_message = render_to_string("content/email.html", context=context)
    # extracts plain text from html message without the tags.
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=None,
        to=[get_email],
    )

    message.attach_alternative(html_message, "text/html")
    message.send()

    email = Email.objects.create(
        subject=subject,
        body="Email sent",
        email=get_email,
    )

    # serializer = EmailSerializer(email)
    # return Response(serializer.data)
    return Response({"Message": "Success"})
