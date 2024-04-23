from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Email
from .serializers import EmailSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db import transaction


# Create your views here.


# Get all your emails from db
@api_view(["GET"])
def get_email(request):
    queryset = Email.objects.all()

    serializer = EmailSerializer(queryset, many=True)
    return Response(serializer.data)
    # return Response({"Message": "Success"})


# Create a new email object
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
