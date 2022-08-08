from authentication.models import Customers
from froala_editor.fields import FroalaField
from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from base.models import *


class ContactUs(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    msg = models.TextField()
    def __str__(self):
        return self.name


class blogModel(BaseModel):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    img = models.ImageField(upload_to='blogs')
    def __str__(self) :
        return self.title


class blogCommentsModel(BaseModel):
    person = models.ForeignKey(Customers, related_name="blog_commenter", on_delete=models.PROTECT)
    blog = models.ForeignKey(blogModel, related_name="blog_comments", on_delete=models.CASCADE)
    comment = models.TextField()


class Products(BaseModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='products')
    description = models.TextField()
    is_top_selling = models.BooleanField(default=False)
    ratings = models.FloatField(default=0)
    def __str__(self):
        return self.name


class ProductReview(BaseModel):
    product = models.ForeignKey(Products, related_name="related_ratings", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, related_name="customer_product_review", on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    review = models.TextField()


# @receiver(pre_save, sender=ProductReview)
# def find_avg_rating(sender, instance, *args, **kwargs):
#     product_obj = instance.product
#     product_obj.ratings = float(ProductReview.objects.filter(product=product_obj).aggregate(Avg("stars")).get("stars__avg"))
#     product_obj.save()