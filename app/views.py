from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from authentication.models import Customers
from cart.models import *
from .models import *
from .threads import send_contact_email

context = {}
context["blog_id"] = settings.BLOG_ID

def homePage(request):
    context["top_selling_products"] = Products.objects.filter(is_top_selling=True)
    return render(request, "main/index.html", context)

def aboutPage(request):
    return render(request, "main/about.html", context)

def contactPage(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            msg = request.POST.get('message')
            thread_obj = send_contact_email(email, name)
            thread_obj.start()
            ContactUs.objects.create(name=name, email=email, msg=msg)
    except Exception as e:
        print(e)
    return render(request, "main/contact.html", context)

def blogPage(request, blog_id):
    try:
        blog_obj = blogModel.objects.get(id = blog_id)
        print(blog_obj)
        context['blog_obj'] = blog_obj
        context['other_blogs'] =  blogModel.objects.all().exclude(id=blog_id)
        context["blog_cmt"] = blog_obj.blog_comments.all()
    except Exception as e:
        print(e)
    return render(request, "main/blog.html", context)

@login_required(login_url='/login/')
def addBlogComment(request, blog_id):
    try:
        if request.method == 'POST':
            blogCommentsModel.objects.create(
                person = Customers.objects.get(email=request.user),
                blog = blogModel.objects.get(id = blog_id),
                comment = request.POST.get('cmt')
            )
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def allProductsPage(request):
    context["products"] = Products.objects.all().order_by("-created_at")
    return render(request, "products/all-products.html", context)

def productPage(request, product_id):
    try:
        product_obj = Products.objects.get(id = product_id)
        context["item_obj"] = product_obj
        context["similar_products"] = Products.objects.all().exclude(id=product_id)
        context["reviews"] = product_obj.related_ratings.all()
        if request.method == 'POST':
            ProductReview.objects.create(
                product = product_obj,
                customer = Customers.objects.get(email=request.user),
                stars = int(request.POST.get('star')),
                review = request.POST.get('review')
            )
            product_obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
    return render(request, "products/product.html", context)

@login_required(login_url='/login/')
def add_to_cart(request, item_id):
    try:
        customer = Customers.objects.get(email=request.user)
        food_obj = Products.objects.get(id=item_id)
        cart_obj, _ = CartModel.objects.get_or_create(owner=customer, is_paid=False)
        if cart_obj.related_cart.filter(item=food_obj).exists():
            cart_item = CartItems.objects.get(cart=cart_obj, item=food_obj)
            cart_item.quantity += 1
            cart_item.save()
        else : 
            CartItems.objects.create(owner=customer ,cart=cart_obj, item=food_obj)
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    try:
        customer = Customers.objects.get(email=request.user)
        food_obj = Products.objects.get(id = item_id)
        cart_obj = CartModel.objects.get(owner = customer, is_paid = False)
        if cart_obj.related_cart.filter(item=food_obj).exists():
            cart_item = CartItems.objects.get(cart = cart_obj, item = food_obj)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.quantity -= 1
                cart_item.save()
                cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/')
def delete_from_cart(request, item_id):
    try:
        customer = Customers.objects.get(email=request.user)
        food_obj = Products.objects.get(id = item_id)
        cart_obj = CartModel.objects.get(owner = customer, is_paid = False)
        if cart_obj.related_cart.filter(item=food_obj).exists():
            cart_item = CartItems.objects.get(cart = cart_obj, item = food_obj)
            cart_item.quantity = 0
            cart_item.save()
            cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))