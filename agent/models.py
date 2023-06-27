from django.db import models

# Create your models here.

class ClientPage(models.Model):
    client_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=2048, blank=True, null=True)
    data = models.TextField()