from django.db import models
import uuid


# Create your models here.
class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=500)
    body = models.CharField(max_length=5000)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " + " + self.subject
