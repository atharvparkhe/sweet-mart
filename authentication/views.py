from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .threads import *
from .models import CustomerAddress, Customers
from django.conf import settings
import uuid

context = {}
context["blog_id"] = settings.BLOG_ID

@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login/')
def addressView(request):
    try:
        if request.method == 'POST':
            user_obj = Customers.objects.get(email = request.user)
            if not user_obj:
                messages.error(request, 'User does not exist.')
                return redirect('signup')
            user_obj.phone = request.POST.get('phone')
            user_obj.save()
            CustomerAddress.objects.create(
                customer = user_obj,
                state = request.POST.get('state'),
                town = request.POST.get('town'),
                country = request.POST.get('country'),
                pincode = request.POST.get('pincode'),
                landmark = request.POST.get('landmark'),
                address = request.POST.get('address')
            )
            return redirect("checkout")
    except Exception as e:
        print(e)
    return render(request, "accounts/address.html", context)


def SignUp(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if Customers.objects.filter(email=email).first():
                messages.info(request, 'This account already exist. Try logging in.')
                return redirect('login')
            else:
                tok = str(uuid.uuid4())
                new_customer = Customers.objects.create(email=email, name=name, token=tok)
                new_customer.set_password(password)
                thread_obj = send_verification_email(email, tok)
                thread_obj.start()
                new_customer.save()
                messages.info(request, 'We have sent you a verification link.\nPlease check your mail.')
    except Exception as e:
        print(e)
        messages.error(request, str(e))
    return render(request, "accounts/signup.html", context)


def Verify(request, tok):
    try:
        user_obj = Customers.objects.filter(token = tok).first()
        if not user_obj:
            messages.error(request, 'User does not exist.')
            return redirect('signup')
        elif user_obj.is_verified:
            messages.success(request, 'Your profile is already verified.')
            return redirect('login')
        user_obj.is_verified = True
        user_obj.save()
        messages.success(request, 'Your account has been verified.')
        return redirect('login')
    except Exception as e :
        print(e)
        messages.error(request, str(e))
    return render(request, "accounts/verify.html", context)


def LogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            customer_obj = Customers.objects.filter(email=email).first()
            if customer_obj is None:
                messages.info(request, 'User does not exists. Please Signup')
                return redirect('signup')
            if not customer_obj.is_verified:
                messages.info(request, 'This profile is not verified. Please Check your mail.')
                return redirect('login')    
            user = authenticate(email=email, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('login')
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
    except Exception as e:
        print(e)
        messages.error(request, str(e))
    return render(request, "accounts/login.html", context)


def Forget(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Customers.objects.get(email=email)
            if not user:
                messages.info(request, 'This user does not exist. Please Signup.')
                return redirect('/signup')
            token = str(uuid.uuid4())
            user.token = token
            thread_obj = send_forgot_link(email, token)
            thread_obj.start()
            user.save()
            messages.info(request, 'We have sent you a link to reset password via mail')
    except Exception as e:
        print(e)
        messages.error(request, str(e))
    return render(request, "accounts/forgot.html", context)


def Reset(request, token):
    try:
        customer_obj = Customers.objects.get(token=token)
        if not customer_obj:
            messages.info(request, 'This user does not exist. Please Signup.')
            return redirect('/signup')
        if request.method == 'POST':
            npw = request.POST.get('npw')
            cpw = request.POST.get('cpw')
            if npw == cpw:
                customer_obj.set_password(cpw)
                customer_obj.save()
                messages.info(request, 'Password Changed successfully.')
                return redirect('/login')
            messages.error(request, 'New Password and Confirm Password dont match.')
            return redirect('/login')
    except Exception as e :
        print(e)
        messages.error(request, str(e))
    return render(request, "accounts/reset.html", context)