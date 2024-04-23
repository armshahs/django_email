from django.urls import path
from .views import create_email, get_email, create_send_email

urlpatterns = [
    path("create_email/", create_email, name="create_email"),
    path("get_email/", get_email, name="get_email"),
    path("create_send_email/", create_send_email, name="create_send_email"),
]
