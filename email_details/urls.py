from django.urls import path
from .views import (
    create_email,
    get_email,
    create_send_email,
    create_send_htmlemail,
    create_send_htmlemail_variables,
)

urlpatterns = [
    path("create_email/", create_email, name="create_email"),
    path("get_email/", get_email, name="get_email"),
    path("create_send_email/", create_send_email, name="create_send_email"),
    path("create_send_htmlemail/", create_send_htmlemail, name="create_send_htmlemail"),
    path(
        "create_send_htmlemail_variables/",
        create_send_htmlemail_variables,
        name="create_send_htmlemail_variables",
    ),
]
