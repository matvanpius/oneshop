from argparse import Action
from base64 import urlsafe_b64decode
from collections import UserDict
import decimal
from itertools import product
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template import context
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from myApp import settings
from .inhernt import cartData
from django.views.decorators.http import require_POST
from .tokens import generate_token
from .models import Fruit, Legumes, Mixed, Oil, Order, OrderItem, Product,All,Mixed, Snack, Spice,Vegetable


def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def products(request):
    return render(request,'products.html')

def vegetable(request):
    veg = Vegetable.objects.all()
    contex = {'veg':veg}
    context = {}
    return render(request,'vegetable.html',context)

def fruit(request):
    fru = Fruit.objects.all()
    context = {'fru':fru}
    return render(request,'fruit.html',context)

def oil(request):
    cook = Oil.objects.all()
    context = {'cook':cook}
    return render(request,'oil.html',context)

def snack(request):
    sna = Snack.objects.all()
    context = {'sna':sna}
    return render(request,'snack.html',context)

def spice(request):
    spy = Spice.objects.all()
    context = {'spy':spy}
    return render(request,'spice.html',context)

def legumes(request):
    legu = Legumes.objects.all()
    context = {'legu':legu}
    return render(request,'legumes.html',context)



def summary(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'summary.html',context)

def item(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    products = Product.objects.all()
    return render(request, "item.html", {'products':products, 'cartItems':cartItems})



def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return render(request, "cart.html", {'items':items, 'order':order, 'cartItems':cartItems})



def main(request):
    context = {}
    return render(request,'main.html',context)

def allproducts(request):
    prod = All.objects.all()
    context = {'prod':prod}
    return render(request,'allproducts.html',context)
    
def packages(request):
    mix = Mixed.objects.all() 
    context = {'mix': mix}
    return render(request,'packages.html',context)



def signup(request):

    if request.method == "POST":

       username = request.POST['username']
       fname = request.POST['fname']
       lname = request.POST['lname']
       email = request.POST['email']
       pas1 = request.POST['pas1']
       pas2 = request.POST['pas2']
         
       if User.objects.filter(username=username):
           messages.error(request ,"Username already exist! Please use other username")
           return redirect('signin')


       if User.objects.filter(email=email):
           messages.error(request, "Email  already exist! Please use other Email")
           return redirect('signin')

       if len(username)>10:
           messages.error(request,'Username must be under 10 charaters.')

       if pas1 != pas1 :
           messages.error(request,"Passwords didn't match!")

       if not username.isalnum():
           messages.error(request,'Username must be Alpha-numeric!')
           return redirect('signup')

        

       myuser = User.objects.create_user(username,email,pas1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.is_active = False
       myuser.save()

       messages.success(request, 'Your Account has been successfully created.We have sent you aconfirmation email, Please confirm your email inorder to activate your account.')
      
       #welcome Email
       subject= "Welcome to oneshop = Django Login !!"
       message= "Hello" + myuser.first_name + "!! \n" + "Welcome to oneshop !! \n Thank you for Visiting our website \n We have also sent you a confirmation Email, Please confirm your Email Address in order to activate your Account.\n\n Thanking you." 
       from_email = settings.EMAIL_HOST_USER
       to_list = [myuser.email]
       send_mail(subject, message, from_email, to_list, fail_silently = True)

       #Email Address comfirmation
       current_site = get_current_site(request)
       email_subject = "Confirm your email @oneshop-Django Login!!"
       message2 = render_to_string('email_confirmation.html',{
           'name':myuser.first_name,
           'domain':current_site.domain,
           'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
           'token': generate_token.make_token(myuser)

       })
       email = EmailMessage(
           email_subject,
           message2,
           settings.EMAIL_HOST_USER,
           [myuser.email],

       )
       email.fail_silently = True
       email.send()

       return redirect('signin')
    
    return render(request,'signup.html')


def signin(request):
    if request.method == "POST":

       username = request.POST['username']
       pas1 = request.POST['pas1']

       user = authenticate(username=username,password=pas1)
       
       if user is not None:
           login(request,user)
           fname = user.first_name
           return render(request,'signup.html',{fname:fname})

       else:
            messages.error(request,"Please enter a correct username and password. Try Again!")
            return redirect('signin')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successful.")
    return redirect('index')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if  myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_activate = True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_fail.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
      orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
       orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
   

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True



def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    

        for item in self.cart.values():
            item['price'] = decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
