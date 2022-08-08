from django.db import models
from base.models import *


class Customers(BaseUser):
    token = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'customer'


class CustomerAddress(BaseModel):
    customer = models.ForeignKey(Customers, related_name="customer_address", on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.CharField(max_length=100)
    town = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="India")