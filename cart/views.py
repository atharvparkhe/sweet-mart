from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decouple import config
from authentication.models import *
from django.contrib import messages
from .models import *
from .threads import generate_invoice
from django.conf import settings
import razorpay

context = {}
context["blog_id"] = settings.BLOG_ID
client = razorpay.Client(auth=(config("PUBLIC_KEY"), config("PRIVATE_KEY")))

@login_required(login_url='/login/')
def cartPage(request):
    user = Customers.objects.get(email=request.user)
    if CartModel.objects.filter(owner=user, is_paid=False).exists():
        cart_obj = CartModel.objects.get(owner=user, is_paid=False)
        context["cart_obj"] = cart_obj
        context["cart_items_obj"] = cart_obj.related_cart.all()
        return render(request, 'cart/cart.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def selectAddress(request):
    try:
        user = Customers.objects.get(email=request.user)
        if request.method == 'POST':
            address_id = request.POST.get('address_id')
            address = CustomerAddress.objects.get(id=address_id)
            cart_obj = CartModel.objects.get(owner=user, is_paid=False)
            cart_obj.address = address
            cart_obj.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/')
def checkoutPage(request):
    try:
        user = Customers.objects.get(email=request.user)
        if not CustomerAddress.objects.filter(customer = user).exists():
            return redirect('address')
        cart_obj = CartModel.objects.get(owner=user, is_paid=False)
        amt = int(cart_obj.total_amt * 100)
        payment = client.order.create({
            'amount' :  amt,
            'currency' : 'INR' ,
            'payment_capture' : 1 
        })
        cart_obj.order_id = payment['id']
        cart_obj.save()
        context["cart_obj"] = cart_obj
        context["cart_items_obj"] = CartItems.objects.filter(cart=cart_obj)
        context["all_address"] = CustomerAddress.objects.filter(customer=user)
        context["key"] = config("PUBLIC_KEY")
        context["order_id"] = payment['id']
    except Exception as e:
        print(e)
    return render(request, 'cart/checkout.html', context)


@login_required(login_url='/login/')
def successPage(request):
    try:
        user = Customers.objects.get(email=request.user)
        cart_obj = CartModel.objects.get(owner=user, is_paid=False)
        payment_credentials = {
            "razorpay_order_id" : request.GET.get("razorpay_order_id"),
            "razorpay_payment_id" : request.GET.get("razorpay_payment_id"),
            "razorpay_signature" : request.GET.get("razorpay_signature")
        }
        check = client.utility.verify_payment_signature(payment_credentials)
        if check:
            return render(request, "cart/failed.html")
        cart_obj.order_id = payment_credentials["razorpay_order_id"]
        cart_obj.payment_id = payment_credentials["razorpay_payment_id"]
        cart_obj.payment_signature = payment_credentials["razorpay_signature"]
        cart_obj.is_paid = True
        cart_obj.save()
        thread_obj = generate_invoice(cart_obj)
        thread_obj.start()
    except Exception as e:
        print(e)
    return render(request, 'cart/success.html', context)

@login_required(login_url='/login/')
def failedPage(request):
    return render(request, 'cart/failed.html', context)

@login_required(login_url='/login/')
def couponApplied(request, cart_id):
    cart_obj = CartModel.objects.get(id = cart_id)
    if request.method == 'POST':
        name = request.POST.get("coupon")
        if Coupons.objects.filter(coupon_name = name).exists() and cart_obj.coupon_applied == False:
            coupon_obj = Coupons.objects.get(coupon_name = request.POST.get("coupon"))
            cart_obj.total_price -= cart_obj.total_price*coupon_obj.coupon_discount_amount
            cart_obj.total_amt = cart_obj.total_price + (0.3 * cart_obj.total_price)
            cart_obj.coupon_applied = True
            cart_obj.save()
            coupon_obj.save()
            messages.success(request, 'Coupon Applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else :
            messages.error(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))