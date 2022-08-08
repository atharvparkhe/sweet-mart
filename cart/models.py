from django.db import models
from base.models import BaseModel
from authentication.models import CustomerAddress, Customers
from app.models import Products
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .manager import *

class CartModel(BaseModel):
    owner = models.ForeignKey(Customers, related_name="related_customer_cart",on_delete=models.PROTECT)
    total_price = models.FloatField(default=0)
    tax = models.FloatField(default=0.3)
    total_amt = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    coupon_applied = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey(CustomerAddress, related_name="selected_address", on_delete=models.CASCADE, null=True, blank=True)

class CartItems(BaseModel):
    owner = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="related_customer_cart_items")
    cart = models.ForeignKey(CartModel, related_name="related_cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Products, related_name="related_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0)

@receiver(pre_save, sender=CartItems)
def get_items_total(sender, instance, *args, **kwargs):
    instance.total = instance.item.price * instance.quantity

@receiver(post_save, sender=CartItems)
def get_total_amt(sender, instance, *args, **kwargs):
    total = 0
    cart_obj = CartModel.objects.get(owner = instance.owner, is_paid=False)
    for i in CartItems.objects.filter(cart=cart_obj):
        total += i.total
    cart_obj.total_price = total
    total += (cart_obj.tax*total)
    cart_obj.total_amt = total
    cart_obj.save()

class Coupons(BaseModel):
    coupon_name = models.CharField(max_length=100, unique=True)
    coupon_discount_amount = models.FloatField(default=0.2)
    use_times = models.PositiveIntegerField(default=10)
    is_deleted = models.BooleanField(default=False)
    objects = CouponManager()
    admin_objects = models.Manager()
    def __str__(self):
        return self.coupon_name

@receiver(pre_save, sender=Coupons)
def coupon_update(sender, instance, *args, **kwargs):
    instance.use_times -= 1
    if instance.use_times < 1:
        instance.is_deleted = True