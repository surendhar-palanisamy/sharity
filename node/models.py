from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.
from base.models import Payment
class Node_block(models.Model):
    payment_header = models.ForeignKey(Payment, on_delete=CASCADE)
    current_hash = models.CharField(max_length=255, blank=True, null=True)
    previous_hash = models.CharField(max_length=225, blank=True)
    nonce = models.CharField(max_length=10, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    cash = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.CharField(max_length=255, blank=True, null=True)