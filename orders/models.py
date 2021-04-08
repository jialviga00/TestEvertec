from django.utils import timezone
from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=80)
    customer_email = models.CharField(max_length=120)
    customer_mobile = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField('Created at', default=timezone.now)
    updated_at = models.DateTimeField('Updated at')
    amount = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    unit_value = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    reference = models.CharField(max_length=20, blank=True, null=True)
    placetopay_request_id = models.CharField(max_length=10, blank=True, null=True)
    placetopay_process_url = models.CharField(max_length=100, blank=True, null=True)
    placetopay_message = models.CharField(max_length=150, blank=True, null=True)