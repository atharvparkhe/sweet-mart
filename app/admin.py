from django.contrib import admin
from .models import *

admin.site.register(blogModel)
admin.site.register(ContactUs)
admin.site.register(blogCommentsModel)
admin.site.register(Products)
admin.site.register(ProductReview)