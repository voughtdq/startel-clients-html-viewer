from django.db import models

# Create your models here.

class ClientPage(models.Model):
    client_id = models.IntegerField(unique=True)
    data = models.TextField()